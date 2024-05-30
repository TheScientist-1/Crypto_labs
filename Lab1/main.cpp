#include "crypto_utils.h"

void display_menu() {
    cout << "-----------------------------------------------\n";
    cout << "Lab 1: Mathematical Operations and Primality Testing\n";
    cout << "-----------------------------------------------\n";
    cout << "Select an option:\n";
    cout << "1 - Start interaction\n";
    cout << "0 - Exit\n";
    cout << "-----------------------------------------------\n";
    cout << "Enter your choice: ";
}

void display_results_modular_exponentiation(ll base, ll exponent, ll modulus, ll result) {
    cout << "-----------------------------------------------\n";
    cout << "Modular Exponentiation\n";
    cout << "Calculation: " << base << "^" << exponent << " % " << modulus << " = " << result << "\n";
    cout << "-----------------------------------------------\n";
}

void display_results_primality(ll n, bool mr_result, bool bpsw_result) {
    cout << "-----------------------------------------------\n";
    cout << "Primality Test Results for " << n << "\n";
    cout << "Miller-Rabin Test: " << (mr_result ? "Prime" : "Not prime") << "\n";
    cout << "Baillie–PSW Test: " << (bpsw_result ? "Prime" : "Not prime") << "\n";
    cout << "Conclusion: " << (bpsw_result ? to_string(n) + " is definitely prime.\n" : to_string(n) + " is not prime.\n");
    cout << "-----------------------------------------------\n";
}

void display_conversions(ll n) {
    cout << "-----------------------------------------------\n";
    cout << "Number Conversions for " << n << "\n";
    cout << "Binary (Base 2)  : " << convertToBase(n, 2) << "\n";
    cout << "Decimal (Base 10): " << convertToBase(n, 10) << "\n";
    cout << "Base64          : " << convertToBase(n, 64) << "\n";
    cout << "-----------------------------------------------\n";
}

void display_generated_primes(int bits, const vector<ll>& primes) {
    cout << "-----------------------------------------------\n";
    cout << "Generated Primes with " << bits << " bits:\n";
    for (ll prime : primes) {
        cout << prime << "\n";
    }
    cout << "-----------------------------------------------\n";
}

int main() {
    while (true) {
        display_menu();
        int choice;
        cin >> choice;
        if (choice == 0) {
            cout << "Exiting the program...\n";
            break;
        }
        if (choice == 1) {
            ll base, exponent, modulus, n;
            int k, bits;
            vector<ll> primes;

            cout << "Modular Exponentiation:\n";
            cout << "Enter base for modular exponentiation: ";
            cin >> base;
            cout << "Enter exponent: ";
            cin >> exponent;
            cout << "Enter modulus: ";
            cin >> modulus;
            ll mod_exp_result = modularExponentiation(base, exponent, modulus);
            display_results_modular_exponentiation(base, exponent, modulus, mod_exp_result);

            cout << "Primality Testing:\n";
            cout << "Enter number to test for primality: ";
            cin >> n;
            cout << "Enter number of iterations for Miller-Rabin Test: ";
            cin >> k;
            bool mr_result = millerRabinPrimalityTest(n, k);
            bool bpsw_result = bailliePSWPrimalityTest(n);
            display_results_primality(n, mr_result, bpsw_result);

            display_conversions(n);

            cout << "Prime Generation:\n";
            cout << "Enter number of bits for prime generation: ";
            cin >> bits;
            primes = generatePrimes(bits);
            display_generated_primes(bits, primes);
        } else {
            cout << "Invalid choice! Please try again.\n";
        }
    }

    return 0;
}
