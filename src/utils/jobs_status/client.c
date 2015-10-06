/* Sample UDP client */

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define IPADDR	256
#define BUF_LEN	10000

int main(int argc, char**argv) {
	int sockfd,n, port;
	struct sockaddr_in servaddr,cliaddr;
	char ipaddr[IPADDR];
	char sendline[BUF_LEN];
	char recvline[BUF_LEN];

	if (argc < 3) {
	  printf("usage:  %s <IP address> <port>\n", argv[0]);
	  exit(1);
	}

	/* get IP address and port */
	strncpy(ipaddr, argv[1], IPADDR-1 );
	port = atoi(argv[2]);

	/* get socket */
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);

	if( sockfd == -1 ) {
		/* socket successfully created */
		printf("Error creating socket.");
		exit(1);
	}

	bzero(&servaddr,sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr(ipaddr);
	servaddr.sin_port = htons(port);

	do {
		if( fgets( sendline, BUF_LEN, stdin ) != NULL ) {
			/* read from stdio and send to socket; */
			sendto(sockfd, sendline, strlen(sendline), 0, (struct sockaddr *)&servaddr,sizeof(servaddr));
		}
	} while ( !feof(stdin) );

	return 0;
}
