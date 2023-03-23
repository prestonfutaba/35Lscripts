#!/bin/bash

#need to change sorted.words to remove the non-ASCII chars like dashes, convert them into a newline. This makes new words in our dictionary. Also, our dictionary is sorted, only contiains ASCII chars and is all lowercase. 

#converts non-ASCII chars to new lines, ignores repeats and takes /usr/share/dict/linux.words as the input
tr -cs 'A-Za-z' '[\n*]' < linux.words |

#converts all uppercase to lowercase
tr '[:upper:]' '[:lower:]' |

#alphabetizes dictionary, outputs into file called sorted.words
 sort -u > sorted.words

#takes input from  /dev/stdin, converts non-ASCII chars to new lines,  ignores repeats
tr -cs 'A-Za-z' '[\n*]' < /dev/stdin |

#converts all uppercase to lowercase
tr '[:upper:]' '[:lower:]' |

#alphabetizes the input file
sort -u |

#compares /dev/stdin and only outputs column 1, words that are unique to /dev/stdin aka words not in the dictionary
comm -23 - sorted.words
