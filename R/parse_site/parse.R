library(XML)
library(plyr)
library(RCurl)

states <- read.csv("states.csv")

for(i in 1:dim(states)[1]){
#for(i in 1:1){
  #Get states
  thisstate <- as.character(states[i,2])
  
  #Get the list of available HUCs for this state
  thisindex = htmlParse(getURL(paste("http://nas.er.usgs.gov/queries/huc8.aspx?state=", thisstate, sep="")))

  dir.create(path=thisstate)
  
  #Parse the area tags that contain the HUC code and names
  theseareas <- xpathApply(thisindex, "//area[@shape = 'polygon']")
  
  HUC <- data.frame(matrix(NA, nrow = 1, ncol = 2))
  
  for(j in 1:length(theseareas)){
    HUC <- rbind(HUC, strsplit(xmlGetAttr(theseareas[[j]], name="title"), ", ")[[1]])
  }
  
  #Omit empty lines
  realHUC <- na.omit(HUC)
  
  #Get data for that HUC and write to a csv file
  for(h in 1:dim(realHUC)[1]){
    thispage <- htmlParse(getURL(paste("http://nas.er.usgs.gov/queries/SpeciesList.aspx?Group=&Status=0&FMB=0&pathway=0&Sortby=1&Size=500&HUCNumber=", realHUC[h,1], sep="")))
    
    thistable <- readHTMLTable(thispage)
    
    writefile <- paste(thisstate, "/", thisstate, "_", realHUC[h,1], "_", realHUC[h,2], ".csv", sep="")
      
    write.table(thistable$ctl00_ContentPlaceHolder1_myGridView, file=writefile, sep=",", row.names=FALSE, col.names=TRUE)
      
  }
  #convert to windows-type text file
  system(paste("todos ", thisstate, "\\/*", sep=""))
}

