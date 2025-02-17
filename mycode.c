
void esll_print(int text) {
    printf(text);
}

char* esll_checkNumber(int esll_number)
{
    if (esll_number%3==0)
    {
        return "fizz";
    }
    else if (esll_number%5==0)
    {
        return "buzz";
    }
    else if (esll_number%5==0 && esll_number%3==0)
    {
        return "fizzbuzz";
}
    return esll_number;
}
void esll_doFizzbuzz(int esll_number)
{
    esll_print(esll_number);
    esll_print(esll_checkNumber);
    esll_print("");
}
void esll_main()
{
    int esll_makeVariableTest = 3;
    esll_doFizzbuzz(5);
    esll_doFizzbuzz(3);
    esll_doFizzbuzz(15);
    esll_doFizzbuzz(2);
}

int main() {
    esll_main();
}

