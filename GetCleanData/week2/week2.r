# week2.r

setwd('~/GitHub/Coursera/GetCleanData/week2')

###
# Question 1
# Pull down info from github api and find date/time when "datasharing" repo was created by user jtleek
###

library(httr)

# get oauth settings for github
oauth_endpoints('github')
myapp<-oauth_app('github', key='ca08045636482650790d', secret='6b636774ba97c633b5cdad7b04388bf72344b94b')
github_token<-oauth2.0_token(oauth_endpoints('github'), myapp)

# pull down info
gtoken<-config(token=github_token)
req<-GET('https://api.github.com/users/jtleek/repos')

# process to readable
json1<-content(req)
library(jsonlite)
json2<-fromJSON(toJSON(json1))

# now we have a dataframe that is easy to read
names(json2) # shows the fields
datasharing_ind<-which(json2$name=='datasharing')
json2$created_at[datasharing_ind] # returns 2013-11-07T13:25:07Z


###
# Question 2
# choose an appropriate sql query (no coding neeed)
###

# download file from URL
# download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06pid.csv', destfile='w2q2.txt', method='curl')

# acs<-read.table('w2q2.txt', sep=',', header=TRUE)

# Which of the following commands will select only the data for the probability weights pwgtp1 with ages less than 50?

# sqldf("select pwgtp1 from acs") # selects all pwgtp1 entries
# sqldf("select * from acs") # selects all data from the table
# sqldf("select pwgtp1 from acs where AGEP < 50") # selects pwgtp1 field for entries where AGEP is less than 50
# sqldf("select * from acs where AGEP < 50") # selects all fields when agep is less than 50

### 
# Question 3
###

# Using the same data frame you created in the previous problem, what is the equivalent function to unique(acs$AGEP)

# sqldf("select unique * from acs") # not sure what this does - perhaps not even proper general sql syntax
# sqldf("select distinct AGEP from acs") # equiv to unique(acs$AGEP)
# sqldf("select distinct pwgtp1 from acs") # equiv to unique(acs$pwgtp1)
# sqldf("select AGEP where unique from acs") # still not sure what unique keyboard does

###
# Question 4
# how many characters are in the 10th, 20th, 30th and 100th lines of HTML from http://biostat.jhsph.edu/~jleek/contact.html
###

url<-'http://biostat.jhsph.edu/~jleek/contact.html'
fullhtml<-readLines(url)
nchar(htmlcode[c(10, 20, 30, 100)]) # returns 45 31 7 25

###
# Question 5
# report sum of the 4th column in https://d396qusza40orc.cloudfront.net/getdata%2Fwksst8110.for
###

download.file('https://d396qusza40orc.cloudfront.net/getdata%2Fwksst8110.for', destfile='w2q5.txt', method='curl')
q5dat<-read.fwf('w2q5.txt', widths=c(14, 5, 9, 4, 9, 4, 9, 5, 4), skip=4, as.is=TRUE) # column widths first guessed by manual inspection in vi, then tuned for misaligned columns
sum(q5dat[,4]) # returns 32426.7