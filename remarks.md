# Remarks

- no error handling in mongo responses (should return True or false if call was successful)
- logging error should use logger.exception and not logger.error. Excpetion methods automatically cathces and print the 
error so no need to say we ant to print it
- create and use custom exceptions in the folder `utils/exceptions`

- stop putting `WARNING` logs everywhere! They should be exclusive to errors that are non critical to running the app
