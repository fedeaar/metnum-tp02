/*
#include "../potencia.h"
#include "cmath"

#define autovalores vector<double>
#define autovectores vector<vector<double>>


double productoInterno(vector<double>& x, vector<double>& y){
    double sum = 0;
    for(int i = 0; i < x.size(); ++i) 
        sum += x[i] * y[i];
    
    return sum;
}


void metodoDeLaPotencia(matriz<double> A, int iteraciones, double tolerancia) {
    int n = A.n(); 

    int k = 0;
    for(int k = 0; k < n; ++k) {
        vector<double> y(n);
        for(int i = 0; i < n; ++i) 
            y[i] = rand();

        bool tolerable = false;
        for(int i = 0; i < iteraciones && !tolerable; ++i) {
            vector<double> next_y = (A * y) * (1 / productoInterno(y, y));
            
            double maxDif = 0;
            for(int j = 0; j < n; ++j) 
                maxDif = max(maxDif, abs(next_y[j] - y[j]));
            if (maxDif <= tolerancia) tolerable = true; 
        }

        double l = productoInterno(y, (A * y)) / productoInterno(y,y);

        // exporto autovalor l, autovector y

        double yty = productoInterno(y, y);
        vector<vector<int>> yyt(n, vector<int>(n));
        for(int i = 0; i < n; ++i) 
            for(int j = 0; j < n; ++j) 
                yyt[i][j] = y[i] * y[j] * (l/yty);
        
        A = A - yty;
    }
    
}
*/
