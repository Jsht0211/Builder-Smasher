# Builder-Smasher

## Basic information

The Builder-Smasher uses deepseek(or gemma for image to text) to do english builder automatically



## How to download the tool?

Go to the release page and click on 'Builder-Smasher.exe' to download the executable file



## How to use it?

You need to have a hugging face token(for authentication) to use the AI
(If you don't know how to get one, a tutorial is available in the executable file. Run it and follow the steps.)

Once you've successfully entered your token, fill in the basic information such as:
-the number of exercises you want to do,
-whether or not to enable image to text, and
-your username and password

After that, you can just be away from keyboard and wait for the exercises to be completed



## How does it work?

The tool first searches for incompleted exercises, once it finds one and the type of the exercise is reading, writing or speaking, it clicks into the exercise and starts do to it. When the exercise is done, the tool goes back to the lesson choosing page and repeat the mentioned steps.



## Special reminders

The AI may not be correct all the time. It will sometimes make a lot of mistakes. Therefore, the accuracy may be a little bit low, but the average accuracy is above 70%

The use of AI **consumes your tokens for inference usage**(not the one for authentication mentioned before)

If the tool suddenly goes back to the lesson choosing page after opening an exercise, don't be worried. This is because you have turned off the image to text feature and the tool finds out that the exercise(most of the time reading) contains passages in form of images. You can simply just ignore it 

The tool will create a file called 'blacklist.json' after you run it. This file keeps the information of the exercises containing image passages(which is mentioned on top). This will save time when you run the tool next time as it will skip all the exercises that cannot be done. It's ok to delete the file, but the tool will waste time clicking into the exercises containing image passages next time(If the file is deleted, it will be created again when you run the tool next time)

If an error appears in the output console, it may be either caused by you running out of tokens, or the AI answering the questions wrongly. Run the file again and enter your token. If the program says that it is an invalid token, that means you have used all of your tokens for inference usage. You can wait till next month when your token quota is reset, or just create a new account. If the program keeps going, that means the AI made mistakes. You can fill in your information again and wait for the tool to help you complete the exercises

The most important thing:
**Make Sure You have the 136.0.7103.93 version of Chrome**, or else the file won't be able to run
