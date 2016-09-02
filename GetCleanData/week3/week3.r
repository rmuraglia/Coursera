# week3.r

setwd('~/GitHub/Coursera/GetCleanData/week3')
library(dplyr)

######
# Q1: pull down Idaho data and get houses greater than 10 acres who sold more than 10k of agriculture products
######

if (!file.exists('w3q1.txt')) {
    download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv', destfile='w3q1.txt', method='curl')
}

q1dat<-read.table('w3q1.txt', sep=',', header=TRUE)
agricultureLogical <- q1dat$ACR==3 & q1dat$AGS==6
which(agricultureLogical)

# answer: 125, 238, 262

######
# Q2: load jpeg and get quantiles
######

library(jpeg)
if (!file.exists('w3q2.jpg')) {
    download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fjeff.jpg', destfile='w3q2.jpg', method='curl')
}
img<-readJPEG('w3q2.jpg', native=TRUE)
quantile(img, probs=c(0.3, 0.8))

# answer: -15259150, -10575416

######
# Q3: GDP matching and ranking
######

if (!file.exists('w3q3A.txt')) {
    download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FGDP.csv', destfile='w3q3A.txt', method='curl')
}
if (!file.exists('w3q3B.txt')) {
    download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FEDSTATS_Country.csv', destfile='w3q3B.txt', method='curl')
}
q3dat1<-read.csv('w3q3A.txt', header=FALSE, skip=5)[1:190,] # use read csv for better handling of quoted commas in GDP col
q3dat2<-read.csv('w3q3B.txt', header=TRUE)
colnames(q3dat1)[c(1, 2, 4, 5)]<-c('CountryCode', 'Ranking', 'Long.Name', 'GDP')

# make merged (drops unmatched)
q3datmerge<-merge(q3dat1, q3dat2, by.x='CountryCode', by.y='CountryCode')

# get total number of matches: two versions, one with magrittr pipes and one with merged df
match(q3dat1$CountryCode, q3dat2$CountryCode) %>% is.na %>% `!` %>% sum
nrow(q3datmerge)

# answer: 189

# sort by GDP and get 13th highest
# fix commas in GDP col
gdp_char<-as.character(q3datmerge$GDP)
gdp_nocomma<-gsub(',', '', gdp_char)
gdp_num<-as.numeric(gdp_nocomma)
q3datmerge<-cbind(q3datmerge, gdp_num)

q3_sorted<-arrange(q3datmerge, desc(gdp_num))
q3_sorted[13, 1:5]

# answer: Spain

#######
# Q4: average GDP ranking for High Income and Low Income groups
#######

group_by(q3_sorted, Income.Group) %>% summarize(mean(as.numeric(as.character(Ranking))))

# answer: 32.9667, 91.91304

######
# Q5: cut GDP in 5 quantiles, table vs income.group. how many are lower-middle income by in 38 highest gdp
######

library(Hmisc)
q3_sorted<-mutate(q3_sorted, gdprank_bins = cut2(as.numeric(as.character(Ranking)), g=5))
table(q3_sorted$gdprank_bins, q3_sorted$Income.Group)

# answer: 5
