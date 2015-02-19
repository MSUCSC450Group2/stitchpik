#include <stdlib.h>
//kMeans function, takes two arrays, image data, and means(color) data, as well as their respective lengths

//Apply palette to image by using closest color distance
//Inputs are image data, a list of colors, and their respective lengths
int* cPalettize(int** imageData, int imageLength, int** colorsList, int colorsLength) {
    int closestNum, closestDistance, tempDistance;
    int i, c;

    int* retImage = (int *) malloc(imageLength * sizeof(int));      

    for(i = 0; i < imageLength; i++) {
        closestNum = 0;
        closestDistance = abs(colorsList[0][0] - imageData[i][0]) +
            abs(colorsList[0][1] - imageData[i][1]) +
            abs(colorsList[0][2] - imageData[i][2]);
       
        for(c = 1; c < colorsLength; c++) {
            tempDistance = abs(colorsList[c][0] - imageData[i][0]) +
                abs(colorsList[c][1] - imageData[i][1]) +
                abs(colorsList[c][2] - imageData[i][2]);

            if(tempDistance < closestDistance) {
                closestDistance = tempDistance;
                closestNum = c;
            }
        }

        retImage[i] = closestNum;
    }
    
    return retImage;
}

int* ckMeans(int** imageData, int imageLength, int** meansList, int meansLength, int imgWidth, int imgHeight ,int numRuns) {
    int i, k;
    int** meansStore = (int **) malloc(meansLength * sizeof(int *));
    for(i = 0; i < meansLength; i++)
        meansStore[i] = malloc(4 * sizeof(int));
    int posX, incrementX, posY, incrementY, imagePos, startX;
    int closestNum, closestDistance, tempDistance;

    for(i = 0; i < meansLength; i++) {
        meansStore[i][0] = 0;
        meansStore[i][1] = 0;
        meansStore[i][2] = 0;
        meansStore[i][3] = 0;
    }

    for(i = 0; i < numRuns; i++) {
        incrementX = imgWidth >> i;
        startX = imgWidth >> (i+1);
        incrementY = imgHeight >> i;
        posY = imgHeight >> (i+1);

        //Take samples from the image at increasing granularity
        //Find the closest mean, and add pixel data to that mean in meansStore
        while(posY < imgHeight) {
            posX = startX; 
            while(posX < imgWidth) {
                imagePos = posY*imgWidth + posX;
                closestNum = 0;
                closestDistance = abs(meansList[0][0] - imageData[imagePos][0]) +
                    abs(meansList[0][1] - imageData[imagePos][1]) +
                    abs(meansList[0][2] - imageData[imagePos][2]);
    
                for(k = 1; k < meansLength; k++) {
                    tempDistance = abs(meansList[k][0] - imageData[imagePos][0]) +
                        abs(meansList[k][1] - imageData[imagePos][1]) +
                        abs(meansList[k][2] - imageData[imagePos][2]);
    
                    if(tempDistance < closestDistance) {
                        closestNum = k;
                        closestDistance = tempDistance;
                    }
                }
                meansStore[closestNum][0] += imageData[imagePos][0];
                meansStore[closestNum][1] += imageData[imagePos][1];
                meansStore[closestNum][2] += imageData[imagePos][2];
                meansStore[closestNum][3] += 1;
                posX += incrementX;
            }
            posY += incrementY;
        }

        //Update the means list
        for(k = 0; k < meansLength; k++) {
            if(meansStore[k][3] != 0) {
                meansList[k][0] = meansStore[k][0] / meansStore[k][3];
                meansList[k][1] = meansStore[k][1] / meansStore[k][3];
                meansList[k][2] = meansStore[k][2] / meansStore[k][3];
            }
        }
    }

    for(i = 0; i < meansLength; i++)
        free(meansStore[i]);
    free(meansStore);

    int* result =  cPalettize(imageData, imageLength, meansList, meansLength);
    return result;
}

