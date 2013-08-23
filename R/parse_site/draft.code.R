fields = list('Images', 'Group', 'Family', 'Scientific Name', 'Common Name', 'Exotic / Native Transplant')
read_node = function(node){
  
  dl = lapply(fields, function(x) xpathSApply(node, 
                                              paste(".//*[@class = ", "'", x, "'", "]", sep = ""), xmlValue))
  tmp = rep(' ', length(dl))
  tmp[sapply(dl, length) == 1] = unlist(dl)
  confidence = xpathSApply(node, './/img', xmlGetAttr, 'alt')
  return(c(tmp, confidence))
}



library(XML)
library(RCurl)
infraspeciesrank = htmlParse(getURL(indexfile))
path=' //*[contains(concat( " ", @class, " " ), concat( " ", "infraspr", " " ))]'
xpathSApply(infraspeciesrank, path)






doc = htmlTreeParse(thisurl, useInternalNodes = T)
doc
xp_expr = "//table/tbody/tr"
nodes = getNodeSet(doc, xp_expr)
nodes
nodes[1]
nodes[[1]]
xp_expr = "//table[@class= 'gridLayout']/tbody/tr"
nodes = getNodeSet(doc, xp_expr)
nodes
xp_expr = "//table[@class= 'gridLayout']/tr"
nodes
nodes = getNodeSet(doc, xp_expr)
nodes
nodes[1]
nodes[1]
fields = list('Images', 'Group', 'Family', 'Scientific Name', 'Common Name', 'Exotic / Native Transplant')
read_node = function(node){
  dl = lapply(fields, function(x) xpathSApply(node,
                                              paste(".//*[@class = ", "'", x, "'", "]", sep = ""), xmlValue))
  tmp = rep(' ', length(dl))
  tmp[sapply(dl, length) == 1] = unlist(dl)
  confidence = xpathSApply(node, './/img', xmlGetAttr, 'alt')
  return(c(tmp, confidence))
}
read_node(nodes)
read_node(nodes[2])
read_node(nodes[[2])
read_node(nodes[[2]])
read_node(nodes[2][1])
nodes[2]
?readHTMLTable
readHTMLTable(doc)
thistable <- readHTMLTable(doc)
thistable$Table1
thistable$ctl00_ContentPlaceHolder1_myGridView
thistable$tblPageNav
docName(doc)
doc





theseareas <- xpathApply(infraspeciesrank, "//area[@shape = 'polygon']")

xmlGetAttr(theseareas[[1]], name="title")

HUC <- data.frame(matrix(NA, nrow = 1, ncol = 2))

for(i in 1:length(theseareas)){
  HUC <- rbind(HUC, strsplit(xmlGetAttr(theseareas[[i]], name="title"), ", ")[[1]])
}

realHUC <- na.omit(HUC)
