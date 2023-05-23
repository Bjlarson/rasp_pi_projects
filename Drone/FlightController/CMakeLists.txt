cmake_minimum_required(VERSION 3.12)

include(pico_sdk_import.cmake)

project(FlightController)

pico_sdk_init()

add_executable(blink_led
   blink_led.c
)

target_link_libraries(blink_led pico_stdlib)

pico_add_extra_outputs(blink_led)