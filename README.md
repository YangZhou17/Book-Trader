# How to deploy and run
* Use git command line to git clone
* Open command line
* Download yarn
* Download vue-cli
* Change the command line location to the folder location
* Enter yarn install
* Enter yarn run serve
* Not yet packaged, no need to build

# About the front-end and back-end debugging mode
* First, due to cross-domain issues, you need to download nginx
* After downloading nginx, open the installation folder, copy the content in backend/nginx.conf into conf/nginx.conf in the nginx folder
* Return to the root directory of the nginx folder, open the command line and run the command ./nginx.exe and keep the terminal open
* Open the front-end service with yarn run serve
* Run backend/app.py
* Open localhost:9000 in the browser to browse the effect, and you can preview the content in time after modifying the file content

# About the framework or tools used for development
* Front-end framework Vue-cli
* Back-end framework Flask
* UI framework Element-plus
* Cross-domain tool nginx

# Contact Information
* Please contact Jasper Wang (jingzhou.wang@yale.edu) if you have any questions regarding installation or running the program
