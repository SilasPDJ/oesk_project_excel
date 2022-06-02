library(decryptr)
# file <- download_captcha("rfb", path = "./img")
# print(file)
args = commandArgs(trailingOnly=TRUE)
img_file <- gsub("&_&", " ", args[1])
final_file <- gsub("&_&", " ", args[2])
print(img_file)
print(final_file)
decrypt(img_file, model = "rfb")

gete <- decrypt(img_file, model = "rfb")
print(gete)
write(gete, file = final_file)

# https://github.com/decryptr/decryptr
# https://gist.github.com/SilasPDJ/16312261811566bfbe1a97d1a23610bc
