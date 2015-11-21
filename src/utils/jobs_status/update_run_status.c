/* Sample UDP client */

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


#define IPADDR	256
#define BUF_LEN	10000

int main(int argc, char**argv) {
	int sockfd, port, pair;
	struct sockaddr_in servaddr;
	char ipaddr[IPADDR];
	char sendline[BUF_LEN];

	if(argc < 3 || argc % 2 != 1) {
	  fprintf(stderr, "usage:  echo ${USER} ${PWD} status | %s "
	         "<IP address> <port> [<IP address> <port>] ...\n",
	         argv[0]);
	  exit(1);
	}

	if(fgets( sendline, BUF_LEN, stdin ) == NULL) {
       fprintf(stderr, "Error: reading stdin");
	}

    for (pair = 1; pair < argc; pair += 2) {
        /* get IP address and port */
        strncpy(ipaddr, argv[pair], IPADDR-1 );
        port = atoi(argv[pair+1]);

        /* get socket */
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);

        if( sockfd == -1 ) {
            /* socket successfully created */
            fprintf(stderr, "Error creating socket for %s:%d",
                    ipaddr, port);
            exit(1);
        }

        bzero(&servaddr,sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        servaddr.sin_addr.s_addr = inet_addr(ipaddr);
        servaddr.sin_port = htons(port);
        sendto(sockfd, sendline, strlen(sendline), 0,
               (struct sockaddr *)&servaddr,sizeof(servaddr));
        close(sockfd);
    }
	return 0;
}
