#ifndef CRYPTO_UTILS_H
#define CRYPTO_UTILS_H

#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <sstream>
#include <iomanip>
#include <random>

typedef unsigned long long ll;
using namespace std;

string convertToBase(ll num, int base);

int calculateJacobiSymbol(long long a, long long b);
ll modularExponentiation(ll base, ll exponent, ll modulus);
vector<ll> generatePrimes(int bits);

bool millerRabinPrimalityTest(ll number, int iterations);
bool bailliePSWPrimalityTest(ll number);
bool lucasPrimalityTest(ll number, long long D, ll P, ll Q);

#endif // CRYPTO_UTILS_H
