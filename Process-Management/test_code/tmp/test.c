#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int query__start(int count){
	printf("hello world!     start %d\n", count);
}

int query__end(int count) {
	printf("hello world!     end  %d\n", count);
}
int main() {
	int count = 10 ;
	while(1) {
		sleep(1) ;
		query__start(count) ;
		query__end(count) ;
		count++ ;
	}
}
