
// Includes
#include "stdio.h"
#include <stdlib.h>
#include <SDL3/SDL.h>

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


float esll_SPEED = 0.01;
float esll_boxX = 100;
float esll_boxY = 100;
void esll_start()
{
}
void esll_draw()
{
    esll_setBackground(100, 200, 100);
    if (esll_pressingKey(">"))
    {
        esll_boxX = esll_boxX+esll_SPEED;
}
    if (esll_pressingKey("<"))
    {
        esll_boxX = esll_boxX-esll_SPEED;
}
    if (esll_pressingKey("^"))
    {
        esll_boxY = esll_boxY-esll_SPEED;
}
    if (esll_pressingKey("v"))
    {
        esll_boxY = esll_boxY+esll_SPEED;
}
    esll_fill(255, 0, 0);
    esll_drawRectangle(esll_boxX, esll_boxY, 100, 100);
}

int main() {
    esllbackend_makeWindow(800, 800);
    esll_start();

    while (true) {
        esll_draw();
        esllbackend_draw();
    }
}

