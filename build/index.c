
// Includes
#include "stdio.h"
#include <stdlib.h>
#include <SDL3/SDL.h>

// Global variables
float esll_deltatime = 0;
float esllbackend_lastTime = 0;

// Functions
void esll_print(const char* text) {
    printf(text);
    printf("\n");
}

// Graphics
SDL_Window *window;
SDL_Renderer *renderer;

void esllbackend_makeWindow(int width, int height) {
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        printf("SDL_Init Error: %s\n", SDL_GetError());
    }

    if (!SDL_CreateWindowAndRenderer("ESLL Window", width, height, SDL_WINDOW_RESIZABLE, &window, &renderer)) {
        printf("Couldn't create window and renderer: %s\n", SDL_GetError());
    }
}

void esllbackend_draw() {
    // Deltatime
    Uint64 currentTime = SDL_GetPerformanceCounter();
    float inbetweenTime = currentTime - esllbackend_lastTime;
    esll_deltatime = inbetweenTime * 1000 / SDL_GetPerformanceFrequency() * 0.1;
    esllbackend_lastTime = SDL_GetPerformanceCounter();

    SDL_Event event;
    SDL_PollEvent(&event);
    if (event.type == SDL_EVENT_QUIT) {
        exit(0);
    }

    SDL_RenderPresent(renderer);
}

// Interactable graphics
void esll_setBackground(int r, int g, int b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
    SDL_RenderClear(renderer);
}

void esll_fill(int r, int g, int b) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);
}

void esll_drawRectangle(float x, float y, float w, float h) {
    SDL_FRect rect = { x, y, w, h };
    SDL_RenderFillRect(renderer, &rect);
}

bool esll_pressingKey(char* key) {
    const bool *keyState = SDL_GetKeyboardState(NULL);

    if (key == " ") {
        return keyState[SDL_SCANCODE_SPACE];
    } else if (key == ">") {
        return keyState[SDL_SCANCODE_RIGHT];
    } else if (key == "<") {
        return keyState[SDL_SCANCODE_LEFT];
    } else if (key == "^") {
        return keyState[SDL_SCANCODE_UP];
    } else if (key == "v") {
        return keyState[SDL_SCANCODE_DOWN];
    }

    return false;
}


float esll_SCREEN_WIDTH = 800;
float esll_SCREEN_HEIGHT = 800;
float esll_SPEED = 10;
float esll_GRAVITY = 0.35;
float esll_JUMP_POWER = 70;
float esll_boxX = 100;
float esll_boxY = 100;
float esll_boxW = 100;
float esll_boxH = 100;
float esll_boxVelocityY = 0;
void esll_start()
{
}
void esll_draw()
{
    esll_setBackground(100, 200, 100);
    esll_boxVelocityY = esll_boxVelocityY+esll_GRAVITY*esll_deltatime;
    if (esll_pressingKey(">"))
    {
        esll_boxX = esll_boxX+esll_SPEED*esll_deltatime;
}
    if (esll_pressingKey("<"))
    {
        esll_boxX = esll_boxX-esll_SPEED*esll_deltatime;
}
    if (esll_pressingKey(" "))
    {
        esll_boxVelocityY = -esll_JUMP_POWER*esll_deltatime;
}
    esll_boxY = esll_boxY+esll_boxVelocityY*esll_deltatime;
    if (esll_boxY+esll_boxH>esll_SCREEN_HEIGHT)
    {
        esll_boxY = esll_SCREEN_HEIGHT-esll_boxH;
        esll_boxVelocityY = 0;
}
    esll_fill(255, 0, 0);
    esll_drawRectangle(esll_boxX, esll_boxY, esll_boxW, esll_boxH);
}

int main() {
    esllbackend_makeWindow(800, 800);
    esll_start();

    while (true) {
        esll_draw();
        esllbackend_draw();
    }
}

