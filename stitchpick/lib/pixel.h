#include <stdlib.h>

int** cPixelate(int** imageData, int imageWidth, int imageHeight, int numColors, int pixelSize) {
    int pixelWidth, pixelHeight;
    int pixelStartX, pixelStartY;
    int* histogram = (int*)malloc(numColors*sizeof(int));
    int maxColor, maxValue;
    int i, u, v, x, y;

    pixelWidth = imageWidth / pixelSize;
    pixelHeight = imageHeight / pixelSize;

    int** pixelArray = (int**)malloc(pixelHeight*sizeof(int*));
    for(i = 0; i < pixelHeight; i++)
        pixelArray[i] = (int *)malloc(pixelWidth*sizeof(int));

    for(y = 0; y < pixelHeight; y++) 
        for(x = 0; x < pixelWidth; x++) {
            pixelStartX = x*pixelSize;
            pixelStartY = y*pixelSize;
            for(i = 0; i < numColors; i++) histogram[i] = 0;
            for(v = pixelStartY; v < pixelStartY + pixelSize; v++)
                for(u = pixelStartX; u < pixelStartX + pixelSize; u++) {
                    histogram[imageData[v][u]] ++;
                }
            maxColor = 0;
            maxValue = histogram[0];
            for(i = 1; i < numColors; i++)
                if(histogram[i] > maxValue) {
                    maxColor = i;
                    maxValue = histogram[i];
                }
            pixelArray[y][x] = maxColor;
        }

    free(histogram);
    return pixelArray;
}
