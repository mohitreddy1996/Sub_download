'''
Movie Subtitle Downloader using subDB API and python script.
Mohit Reddy
29/12/2015
00:05

'''
import sys
import os
import urllib2
import hashlib
import time

# hash function used to encode the first and the last 64 KB of the video file and check for the best solution in the database.
def get_hash(name):
	readsize=64*1024
	with open(name,'rb') as f:
		size=os.path.getsize(name)
		data=f.read(readsize)
		f.seek(-readsize,os.SEEK_END)
		data+=f.read(readsize)
	return hashlib.md5(data).hexdigest()

# file extensions.
file_extensions=[".webm",".mkv",".flv",".vob",".ogv",".drc",".gif",".avi",".wmv",".mov",".rm",".mp4",".mpg",".mpeg",".3gp"]

# to check if a the srt file is already present / the file given as a command line argument is a video file or not / download the subtitle.
def getsub(fname):
	rows,columns = os.popen('stty size','r').read().split()
	rows=int(rows)
	strname=fname
	# remove the file extension from the filename.
	for i in file_extensions:
		strname=strname.replace(i,"")
	# file the file extension is not a present in file_extensions ,i.e not a video file.
	if(strname==fname):
		for i in range(i,rows):
			print "*",
		print ""
		print "\t\tNot a Video file !!"
		for i in range(i,rows):
			print "*",
		exit()

	# get the hashed value using the hash function.
	hash_video=get_hash(fname)

	# append the file extension .str
	strname+=".srt"

	# check if the .str for the movie already exists.
	if os.path.isfile(strname):
		for i in range(0,rows):
			print "*",
		print ""
		print "\t\tSubtitles Already Exists !!"
		for i in range(0,rows):
			print "*",
		print "\n"
		return

	# prepare the headers and the url.
	headers={'User-Agent':'SubDB/1.0 (mohit/0.1; http://github.com/mohitreddy1996/Sub_download)'}

	url="http://api.thesubdb.com/?action=download&hash="+hash_video+"&langauge=en"

	# check if the subtitles are present. if present write them in the str file and store in the same directory,else print Subtitles not found.
	try:
		reqst=urllib2.Request(url,'',headers)
		response=urllib2.urlopen(reqst).read()
		file_obj=open(strname,'wb')
		file_obj.write(response)
		file_obj.close()
		for i in range(0,rows):
			print "*",
		print ""
		print "\t\tSubtitles Successfully Downloaded !!"
		for i in range(0,rows):
			print "*",
		print "\n"
	except:
		for i in range(0,rows):
			print "*",
		print ""
		print "\t\tSubtitle Not found for ",fname
		for i in range(0,rows):
			print "*",
		print "\n"
		return
	

def main():
	rows,columns = os.popen('stty size','r').read().split()
	rows=int(rows)
	# if the filename is provided in the command line arguments.
	if(len(sys.argv)<2):
		for i in range(0,rows):
			print "*",
		print ""
		print "\t\tFilename missing"
		for i in range(0,rows):
			print "*",
		exit()
	else:
		getsub(sys.argv[1])
		for i in range(0,rows):
			print "*",
		print ""
		print "\t\tENJOY THE MOVIE !!"
		for i in range(0,rows):
			print "*",
		print "\n"
		time.sleep(3)
		# runs the terminal command to run the movie after checking if the subtitle was downloaded or not using VLC Player.
		cmd='vlc '+sys.argv[1]
		fp=os.popen(cmd)
		
if __name__=='__main__':
	main()

