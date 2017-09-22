#!/usr/bin/env Rscript

# used like this:
# Rscript code/filterMissings.R data/transposed_final.csv data/filtered.csv

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
	stop("At least two argument must be supplied (inputfile, outputfile).", call.=FALSE)
} else if (length(args)==1) {
	stop("Please specify the outputfile location.", call.=FALSE)
}

threshold <- 0.1

data <- read.csv(args[1], header = TRUE)

loopCount <- 1

missingPercentageCols <- colMeans(is.na(data))

filterListCols <- missingPercentageCols < threshold

cat("Loop number",loopCount,":\n")
cat("Found" , (dim(data)[2] - sum(filterListCols)) , "cols with too few values\n")
flush.console()

data <- data[filterListCols]

repeat{

	missingPercentageRows <- rowMeans(is.na(data))

	filterListRows <- missingPercentageRows < threshold

	cat("Found" , (dim(data)[1] - sum(filterListRows)) , "rows with too few values\n")
	flush.console()

	if (dim(data)[1] == sum(filterListRows)) {
		cat("No more rows found with too few values")
		# break because cols were already filtered and no more rows were found
		break
	}

	data <- data[filterListRows,]

	loopCount <- loopCount + 1

	missingPercentageCols <- colMeans(is.na(data))

	filterListCols <- missingPercentageCols < threshold

	cat("Loop number",loopCount,":\n")
	cat("Found" , (dim(data)[2] - sum(filterListCols)) , "cols with too few values\n")
	flush.console()

	if (dim(data)[2] == sum(filterListCols)) {
		cat("No more cols found with too few values")
		# break because rows were already filtered and no more cols were found
		break
	}

	data <- data[filterListCols]
}

write.csv(data, file=args[2], row.names=FALSE, na="")