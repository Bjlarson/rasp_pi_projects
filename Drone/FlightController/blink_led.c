#include "pico/stdlib.h"

int main(){
    // Initialise GPIO - Green LED is connected to pin 25
    gpio_init(25);
    gpio_set_dir(25, GPIO_OUT);

    // Infinite Loop
    while (1)
    {
        gpio_put(25, 1);// Set pin 25 High
        sleep_ms(500);// .5s delay
        gpio_put(25,0);// set pin 25 Low
        sleep_ms(500); //.5 dealy
    }
    
}