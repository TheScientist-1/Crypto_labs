#include "crypto_utils.h"

typedef unsigned long long ll;
using namespace std;

ll modularExponentiation(ll base, ll exponent, ll modulus) {
    ll result = 1;
    while (exponent > 0) {
        if (exponent & 1) result = result * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return result;
}

bool millerRabinPrimalityTest(ll number, int iterations) {
    if (number < 4) return number > 1;
    if (!(number & 1)) return false;

    ll d = number - 1;
    while ((d & 1) == 0) d >>= 1;

    random_device rd;
    mt19937_64 gen(rd());
    uniform_int_distribution<ll> dist(2, number - 2);

    for (int i = 0; i < iterations; ++i) {
        ll a = dist(gen);
        ll x = modularExponentiation(a, d, number);
        if (x == 1 || x == number - 1) continue;

        bool pass = false;
        for (; d != number - 1; d <<= 1) {
            x = x * x % number;
            if (x == 1) return false;
            if (x == number - 1) {
                pass = true;
                break;
            }
        }
        if (!pass) return false;
    }
    return true;
}

int calculateJacobiSymbol(long long a, long long b) {
    if (b <= 0 || (b & 1) == 0) return 0;
    int s = 1;
    if (a < 0) {
        a = -a;
        if (b % 4 == 3) s = -s;
    }
    while (a != 0) {
        while ((a & 1) == 0) {
            a >>= 1;
            if (b % 8 == 3 || b % 8 == 5) s = -s;
        }
        swap(a, b);
        if (a % 4 == 3 && b % 4 == 3) s = -s;
        a %= b;
    }
    return (b == 1) ? s : 0;
}

bool lucasPrimalityTest(ll number, long long D, ll P, ll Q) {
    ll d = number + 1, s = 0;
    while ((d & 1) == 0) {
        s++;
        d >>= 1;
    }
    ll U = 1, V = P;
    ll Qk = Q;

    for (ll mask = 1ULL << (63 - __builtin_clzll(d)); mask; mask >>= 1) {
        U = U * V % number;
        V = (V * V - 2 * Qk) % number;
        Qk = Qk * Qk % number;

        if (d & mask) {
            ll U_next = (U * P + V) % number;
            ll V_next = (V * P + U * D) % number;
            U = U_next;
            V = V_next;
            Qk = Qk * Q % number;
        }
    }

    if (U == 0 || V == 0) return true;
    for (ll i = 0; i < s; ++i) {
        V = (V * V - 2 * Qk) % number;
        if (V == 0) return true;
        Qk = Qk * Qk % number;
    }

    return false;
}

bool bailliePSWPrimalityTest(ll number) {
    if (number < 2) return false;
    if (number < 4 || number % 2 == 0) return number == 2;

    if (!millerRabinPrimalityTest(number, 1)) {
        cout << number << " failed Miller-Rabin pre-test" << endl;
        return false;
    }

    long long D = 5, sign = 1;
    while (calculateJacobiSymbol(D, number) != -1) {
        D = D + sign * 2;
        sign = -sign;
    }

    return lucasPrimalityTest(number, D, 1, (1 - D) / 4);
}

string convertToBase(ll num, int base) {
    if (base == 2) return bitset<64>(num).to_string();
    else if (base == 10) return to_string(num);
    else if (base == 64) {
        const char* chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
        string result;
        do {
            result = chars[num % 64] + result;
            num /= 64;
        } while (num);
        return result.empty() ? "0" : result;
    }
    return "";  // Default case for unexpected base
}

vector<ll> generatePrimes(int bits) {
    vector<ll> primes;
    ll start = 1ULL << (bits - 1);
    ll finish = (1ULL << bits) - 1;
    for (ll candidate = start; candidate <= finish; ++candidate) {
        if (millerRabinPrimalityTest(candidate, 100)) primes.push_back(candidate);
    }
    return primes;
}
