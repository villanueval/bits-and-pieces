#Tests from vignette
#http://cran.r-project.org/web/packages/twitteR/vignettes/twitteR.pdf
library(twitteR)

#Setting OAuth
require(ROAuth)
twitter_conskey <-""
twitter_conssecret <- ""
twitter_requesttokenURL <- "https://api.twitter.com/oauth/request_token"
twitter_authorizeURL <- "https://api.twitter.com/oauth/authorize"
twitter_accesstokenURL <- "https://api.twitter.com/oauth/access_token"

cred <- OAuthFactory$new(consumerKey=twitter_conskey, consumerSecret=twitter_conssecret, requestURL=twitter_requesttokenURL, accessURL=twitter_accesstokenURL, authURL=twitter_authorizeURL)

cred$handshake()

registerTwitterOAuth(cred)

#save OAuth object, so no need to create it again lates
save(cred, file="OAuth.twitter.RData")
# load with >> load("OAuth.twitter.RData")

twits <- searchTwitter('#cran', n=500)
twits <- twListToDF(twits)
Encoding(twits$text) <- "latin1"

zz <- getCurRateLimitInfo()
zz$hourlyLimit

