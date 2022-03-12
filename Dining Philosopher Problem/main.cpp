//
// Example from: http://www.amparo.net/ce155/sem-ex.c
//
// Adapted using some code from Downey's book on semaphores
//
// Compilation:
//
//       g++ main.cpp -lpthread -o main -lm
// or 
//      make
//

#include <unistd.h>     /* Symbolic Constants */
#include <sys/types.h>  /* Primitive System Data Types */
#include <errno.h>      /* Errors */
#include <stdio.h>      /* Input/Output */
#include <stdlib.h>     /* General Utilities */
#include <pthread.h>    /* POSIX Threads */
#include <string.h>     /* String handling */
#include <semaphore.h>  /* Semaphore */
#include <iostream>
using namespace std;

/*
 This wrapper class for semaphore.h functions is from:
 http://stackoverflow.com/questions/2899604/using-sem-t-in-a-qt-project
 */
 
 
 
class Semaphore {
public:
    // Constructor
    Semaphore(int initialValue)
    {
        sem_init(&mSemaphore, 0, initialValue);
    }
    // Destructor
    ~Semaphore()
    {
        sem_destroy(&mSemaphore); /* destroy semaphore */
    }
    
    // wait
    void wait()
    {
        sem_wait(&mSemaphore);
    }
    // signal
    void signal()
    {
        sem_post(&mSemaphore);
    }
    
    
private:
    sem_t mSemaphore;
};

const Semaphore Mutex(1);

class LightSwitch{
public:
     void lock(Semaphore);
     void unlock (Semaphore);
   private:
   int readers = 0;
   Semaphore Mutex1 = Mutex;
 };

void LightSwitch:: lock (Semaphore roomE) {
        Mutex1.wait();
        readers += 1;
        if (readers == 1) {
            roomE.wait();
            }
            Mutex1.signal();
	}

void LightSwitch::unlock(Semaphore roomE){
        Mutex1.wait();
        readers= 1;
        if (readers == 0){
        roomE.wait();
        }
        Mutex1.signal();
} 




/* global vars */
const int bufferSize = 5;
const int numReaders = 5; 
const int numWriters = 5; 

/* semaphores are declared global so they can be accessed
 in main() and in thread routine. */
//Semaphore Mutex(1);
Semaphore Spaces(bufferSize);
Semaphore Items(0);
Semaphore turnstile(1);
Semaphore roomEmpty(1);
LightSwitch readSwitch;
LightSwitch writeSwitch;
Semaphore noReaders(1);
Semaphore noWriter(1);
Semaphore footman(4);
Semaphore fork1(1);
Semaphore fork2(1);
Semaphore fork3(1);
Semaphore fork4(1);
Semaphore fork5(1);
Semaphore forks[5]={fork1,fork2,fork3,fork4,fork5};



void *Writer ( void *threadID)
{
	// Thread number
	int x= (long) threadID;
	while (1)
	{
	   turnstile.wait();
	   roomEmpty.wait();
	   printf ("Writer %d: writing \n", x);
	   fflush(stdout);
	   turnstile.signal();
	   roomEmpty.signal();
	   sleep(3);
	   }
}

void *Writer_2 ( void *threadID)
{
	// Thread number
	int x= (long) threadID;
	while (1)
	{

	   writeSwitch.lock(noReaders);
           noWriter.wait();
	   printf ("Writer %d: writing \n", x);
	   fflush(stdout);
	   noWriter.signal();
	   writeSwitch.unlock(noReaders);
	   sleep(3);
	   }
}
	   
	   
void *Reader ( void *threadID)
{
   // Thread number
   int x = (long) threadID;
   while (1 )
   {
	turnstile.wait();
	turnstile.signal();
	readSwitch.lock(roomEmpty);
	printf( "Reader %d: reading\n", x);
	fflush(stdout);
	readSwitch.unlock(roomEmpty);
	sleep(3);
}
}
void *reader_2( void *threadID)
{
   // Thread number
   int x = (long) threadID;
   while (1 )
   {
   	noReaders.wait();
	readSwitch.lock(noWriter);
	noReaders.signal();
	printf( "Reader %d: reading\n", x);
	fflush(stdout);
	readSwitch.unlock(noWriter);
	sleep(3);
}
}
int right(int threadID)
{
	return((threadID+1)%5);
}

int left(int threadID)
{
	return threadID;
}


void get_fork(int i)
{
       footman.wait(); 
       forks[right(i)].wait(); 
       forks[left(i)].wait();
}

void put_fork(int i)
{     
       forks[right(i)].signal();
       forks[left(i)].signal();
       footman.signal();
}

void think(int input)
{
printf( "Philosopher %d is thinking\n", input);
return;
}

void eat(int input)
{
printf( "Philosopher %d is eating\n", input);
return;
}

void *philosopher(void *threadID)
{
     int value=(long)threadID;
     while(1)
     {
     	get_fork(value);
     	eat(value);
     	sleep(0);
     	put_fork(value);
     	think(value);
     	sleep(0);
     
     }
}


void deadlock(int i)
{
     if (i == 4){
	forks[right(i)].wait();
	forks[left(i)].wait();
	}
     else{
	forks[left(i)].wait();
	forks[right(i)].wait();
	}
}

void put_fork_2(int i)
{
       forks[right(i)].signal(); 
       forks[left(i)].signal();
    
}


void *philosopher_2(void *threadID)
{
     int value=(long)threadID;
     while(1)
     {
     	deadlock(value);
     	eat(value);
     	sleep(2);
     	put_fork_2(value);
     	think(value);
     	sleep(2);
     
     }
}





int main(int argc, char **argv )
{
switch(std::stoi(argv[1])){


    case 1:
    		pthread_t writerThread[ numWriters ];
                pthread_t readerThread[ numReaders ];

    // Create the Writter 
	    	for( long p = 0; p < numWriters; p++ )
	    	{
		int rc = pthread_create ( &writerThread[ p ], NULL, 
		                          Writer, (void *) (p+1) );
		if (rc) 
			{
		    printf("ERROR creating writer thread # %ld; \
		            return code from pthread_create() is %d\n", p, rc);
		    exit(-1);
			}
	    		}

		    // Create the reader 
		    for( long c = 0; c < numReaders; c++ )
		    {
			int rc = pthread_create ( &readerThread[ c ], NULL, 
				                  Reader, (void *) (c+1) );
			if (rc) {
			    printf("ERROR creating reader thread # %ld; \
				    return code from pthread_create() is %d\n", c, rc);
			    exit(-1);
			}
		    }

		    printf("Main: program completed. Exiting.\n");


		    // To allow other threads to continue execution, the main thread 
		    // should terminate by calling pthread_exit() rather than exit(3). 
		    pthread_exit(NULL); 
		    break;
	    
    case 2:
                   pthread_t writerThread_2[ numWriters ];
                   pthread_t readerThread_2[ numReaders ];
    
		    // Create the Writter 
		    for( long p = 0; p < numWriters; p++ )
		    {
			int rc = pthread_create ( &writerThread_2[ p ], NULL, 
				                  Writer_2, (void *) (p+1) );
			if (rc) 
			{
			    printf("ERROR creating writer thread # %ld; \
				    return code from pthread_create() is %d\n", p, rc);
			    exit(-1);
			}
		    }

		    // Create the reader 
		    for( long c = 0; c < numReaders; c++ )
		    {
			int rc = pthread_create ( &readerThread_2[ c ], NULL, 
				                  reader_2, (void *) (c+1) );
			if (rc) {
			    printf("ERROR creating reader thread # %ld; \
				    return code from pthread_create() is %d\n", c, rc);
			    exit(-1);
			}
		    }

		    printf("Main: program completed. Exiting.\n");


		    // To allow other threads to continue execution, the main thread 
		    // should terminate by calling pthread_exit() rather than exit(3).  

		    break;
    
    case 3:
                    pthread_t writerThread_3[ numWriters ];
               
		     for( long p = 0; p < numWriters; p++ )
		    {
			int rc = pthread_create ( &writerThread_3[ p ], NULL, 
				                  philosopher, (void *) (p+1) );
			if (rc) 
			{
			    printf("ERROR creating writer thread # %ld; \
				    return code from pthread_create() is %d\n", p, rc);
			    exit(-1);
			}
		    }break;
    
    case 4:
                   pthread_t writerThread_4[ numWriters ];
		    for( long p = 0; p < numWriters; p++ )
		    {
			int rc = pthread_create ( &writerThread_4[ p ], NULL, 
				                  philosopher_2, (void *) (p+1) );
			if (rc) 
			{
			    printf("ERROR creating writer thread # %ld; \
				    return code from pthread_create() is %d\n", p, rc);
			    exit(-1);
			}
		    }
		    break;
    default:
                   break;
    }
    
 
pthread_exit(NULL);

} 






