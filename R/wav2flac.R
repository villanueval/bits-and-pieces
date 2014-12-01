wav2flac <- function (file, reverse = FALSE, overwrite = FALSE, exename = NULL, path2exe = NULL) {
  
  #Check if input file exists
  if (file.exists(file) == FALSE){
    stop(paste("File", file, "was not found."))
  }
  
  flac_args = ""
  #If overwrite, pass argument to overwrite to flac
  if (overwrite){
    flac_args = "-f"
  }
  
  #If reverse
  if (reverse){
    flac_args = "-d"
  }
  
  #if both
  if (overwrite && reverse){
    flac_args = "-df"
  }
  
  #check if target exists
  if (reverse){
    target_file = paste(substr(file, 0, nchar(file) - 4), "wav", sep="")
  }else{
    target_file = paste(substr(file, 0, nchar(file) - 3), "flac", sep="")
  }
  
  #Return error if overwrite is false, but the target file exists
  if (overwrite == FALSE && file.exists(target_file)){
    stop(paste("Target file", target_file, "exists. Please set 'overwrite' to TRUE if you want to overwrite the file."))
  }
      
    
	if (.Platform$OS.type == "unix") {
	  #For UNIX, LINUX, MAC
		if (missing(exename)) 
			exename <- "flac"
		if (missing(path2exe)) {
			exe <- exename
		}
		else {
			exe <- paste(path2exe, exename, sep = "/")
		}
		
		#Give specific error when flac is not found
		if (system(paste(exe, "-v"), ignore.stderr = TRUE)!=0){
			stop("FLAC program was not found.")
		}
    
    #Run command
		e <- system(paste(exe, flac_args, file, sep=" "), ignore.stderr = TRUE)
	}
	if (.Platform$OS.type == "windows") {
    #WINDOWS
		if (missing(exename)) 
			exename <- "flac.exe"
		if (missing(path2exe)) {
			#Drive letter in caps, otherwise it causes an error
			exe <- paste("C:/Program Files/FLAC/", exename, sep = "")
			if (!file.exists(exe)){
				#For 64bit systems
				exe <- paste("C:/Program Files (x86)/FLAC/", exename, sep = "")
			}
		}
		else {
			exe <- paste(path2exe, exename, sep = "/")
		}
		#Give specific error when flac is not found
		if (!file.exists(exe)){
			stop("FLAC program was not found.")
		}
		
    #Run command
		e <- system(paste(shQuote(exe), flac_args, shQuote(file, type = "cmd"), sep = " "), ignore.stderr = TRUE)
	}
  
  #Was there an error?
	if (e != 0) {
		stop(paste("File has a wrong format/encoding"))
	}
	if (overwrite) {
		unlink(file)
	}
}