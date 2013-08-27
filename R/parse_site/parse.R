library(XML)
library(plyr)
library(RCurl)

#Read list of states
states <- read.csv("states.csv")

#where to save the data
mainwritefile <- "results.csv"

for(i in 1:dim(states)[1]){
#for(i in 1:2){
  #Get states
  thisstate <- as.character(states[i,2])
  
  #Get the list of available HUCs for this state
  thisindex = htmlParse(getURL(paste("http://nas.er.usgs.gov/queries/huc8.aspx?state=", thisstate, sep="")))

  #Create dir for each state
  dir.create(path=thisstate)
  
  #Parse the area tags that contain the HUC code and names
  theseareas <- xpathApply(thisindex, "//area[@shape = 'polygon']")
  HUC <- data.frame(matrix(NA, nrow = 1, ncol = 2))
  for(j in 1:length(theseareas)){
    #Get the "title" attribute that contains the HUC and the name
    HUC <- rbind(HUC, strsplit(xmlGetAttr(theseareas[[j]], name="title"), ", ")[[1]])
  }
  
  #Omit empty lines
  realHUC <- na.omit(HUC)
  
  #Get data for that HUC and write to a csv file
  for(h in 1:dim(realHUC)[1]){
    thispage <- htmlParse(getURL(paste("http://nas.er.usgs.gov/queries/SpeciesList.aspx?Group=&Status=0&FMB=0&pathway=0&Sortby=1&Size=500&HUCNumber=", realHUC[h,1], sep="")))
    
    thistable <- readHTMLTable(thispage)
    
    #If the HUC has data, then write to file, otherwise don't do anything
    if(!is.null(thistable$ctl00_ContentPlaceHolder1_myGridView)){
      #Add the HUC and name to the data.frame
      tabletowrite <- cbind(thistable$ctl00_ContentPlaceHolder1_myGridView, thisstate, realHUC[h,1], realHUC[h,2])
      
      names(tabletowrite) <- c(names(tabletowrite)[1:8], "State", "HUC", "Name")
      
      #Only use these columns
      keeps <- c("Group", "Family", "Scientific Name", "Common Name", "Native Habitat", "Exotic / Native Transplant", "State", "HUC", "Name")
      tabletowrite <- tabletowrite[keeps]
      
      writefile <- paste(thisstate, "/", thisstate, "_", realHUC[h,1], "_", realHUC[h,2], ".csv", sep="")
      
      #If result file doesn't exist, create and add column names on first row
      if (!file.exists(mainwritefile)){
        write.table(tabletowrite, file=mainwritefile, sep=",", row.names=FALSE, col.names=TRUE, append=TRUE)
      }else{
        #Just append data, don't add column names
        write.table(tabletowrite, file=mainwritefile, sep=",", row.names=FALSE, col.names=FALSE, append=TRUE)
        }
      write.table(tabletowrite, file=writefile, sep=",", row.names=FALSE, col.names=TRUE, append=FALSE)
      }
  }
  #Uncomment these two lines to convert the files to windows-type text file
  system(paste("todos ", mainwritefile, sep=""))
  system(paste("todos ", thisstate, "\\/*", sep=""))
}

