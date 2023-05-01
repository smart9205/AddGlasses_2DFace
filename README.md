1. install dependencies

imutils
numpy
dlib

**: To install dlib, first need to install CMake and Visual C++
Reference: https://www.geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/


2. run command

put the images to test in the root folder of project.

run below command.

python run.py --image <Image Name> --attr <attributes number(1 or 2)>

ex: 

python run.py --image 11.jpg --attr 2

<table>
  <tr>
    <td><img src="result.jpg" alt="Image 1" height="200"></td>
    <td><img src="result1.jpg" alt="Image 3" height="200"></td>
  </tr>
</table>
