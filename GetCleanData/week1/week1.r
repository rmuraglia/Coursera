# week1.r

setwd('~/GitHub/Coursera/GetCleanData/week1')

###
# Question 1
###

# download file from URL
download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv', destfile='w1q1.txt', method='curl')

# import file to R
q1dat<-read.table('w1q1.txt', sep=',', header=TRUE)

# how many properties are worth more than 1 million dollars?
length(which(q1dat$VAL == 24))

## alternate solution
library(data.table)
q1DT<-as.data.table(q1dat)
sum(q1DT[,VAL==24], na.rm=TRUE)

###
# Question 3
###

download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FDATA.gov_NGAP.xlsx', destfile='w1q3.xlsx', method='curl')

library(xlsx)
q3dat<-read.xlsx('w1q3.xlsx', sheetIndex=1, rowIndex=c(18:23), colIndex=c(7:15))
sum(q3dat$Zip*q3dat$Ext,na.rm=T)

###
# Question 4
###

library(XML)
q4xml<-xmlTreeParse('http://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Frestaurants.xml', useInternal=TRUE)
q4root<-xmlRoot(q4xml)
zipcodes<-xpathSApply(q4root, "//zipcode", xmlValue)
length(which(zipcodes==21231))