#include "gtest-1.8.1/gtest.h"

#include "../src/IO.h"
#include "../src/potencia.h"
#include "../src/matriz/matriz_base.h"


class PotenciaTest : public testing::Test {
protected:
    string basedir;
    double epsilon;
    void SetUp() override {
        basedir = "../../tests/";
        epsilon = 1e-4;
    }

    bool base_test(const string &in, const string &out);
};


bool PotenciaTest::base_test(const string &in, const string &out) {
    IO::potencia::out_file expected = IO::potencia::read_out(basedir + out);
    matriz<base> mat = IO::read_matriz<base>(basedir + in);
    pair<vector<double>, matriz<base>> solucion = deflacion<base>(mat, expected.n, expected.niter, expected.tol);

    bool res = (solucion.first.size() == expected.n);
    for (size_t i = 0; i < expected.n && res; ++i) {
        res = std::abs(solucion.first[i] - expected.solucion[i]) < epsilon;
    }
    matriz<base> diag   = diagonal<base>(solucion.first);
    matriz<base> lambda = solucion.second * diag;
    matriz<base> vect   = mat * solucion.second;
    res = vect.eq(lambda, epsilon);

    return res;
}


TEST_F(PotenciaTest, tests_diagonal) {
    for (int i = 1; i < 11; ++i) {
        string test = "diagonal_" + to_string(i);
        EXPECT_TRUE(base_test(test + ".txt", test + ".autovalores.out"));
    }
}


TEST_F(PotenciaTest, tests_householder) {
    for (int i = 1; i < 11; ++i) {
        string test = "householder_" + to_string(i);
        EXPECT_TRUE(base_test(test + ".txt", test + ".autovalores.out"));
    }
}


TEST_F(PotenciaTest, tests_sdp) {
    for (int i = 1; i < 11; ++i) {
        string test = "sdp_" + to_string(i);
        EXPECT_TRUE(base_test(test + ".txt", test + ".autovalores.out"));
    }
}


TEST_F(PotenciaTest, simetrico) {
    string test = "simetrico";
    EXPECT_TRUE(base_test(test + ".txt", test + ".autovalores.out"));
}
