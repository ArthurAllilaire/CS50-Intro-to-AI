## Experimentation with...

### Convolutional and pooling layers
For the below the dropout was set to 0.5 and I had 1 hidden layer with 128 units.
Different numbers of layers, tried convolution and pooling once, with accuracy of 0.94, then twice with accuracy of 0.974, so a noticeable increase in accuracy, the second convolutional network tests 64 filters as there are less input pixel values as already pooled once.

I also changed the size of the kernels and filters. After the default of 2x2 Max pool, I then tried 3x3 max pool, this gave an accuracy of 0.94 but ran a lot faster. Didn't try any higher as getting rid of detail won't increase accuracy.

For the filters in Conv2D, I tried 2x2 for the first one, this decreased accuracy to 0.967, so I reverted the change. I then tried 4x4 and got accuracy of 0.95 so I reverted that change too.

### Hidden layers
For the hidden layers I tried to double the amount of units, to 256, this gave a decrease in accuracy to 0.94. So I then tried to halve 128 to 64, this gave an accuracy of 0.91. Lastly I tried 100 units, this gave an accuracy of 0.97, so kept 128.

Then I tried two layers of 64 neurons, which gave an accuracy of 0.98 so I kept that.

### Dropout

For the dropout, there is a lower risk of overfitting due to the two convolution steps, therefore I tried to drop the dropout to 0.3, with accuracy of 0.96. Then tried 0.6, which gave an accuracy of 0.98, so kept 0.6.

Overall I got the accuracy to 0.98 at the highest.