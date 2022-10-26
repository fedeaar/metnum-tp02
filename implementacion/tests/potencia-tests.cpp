#include "gtest-1.8.1/gtest.h"

#include "../src/IO.h"
#include "../src/potencia.h"
#include "../src/matriz/matriz_base.h"


class PotenciaTest : public testing::Test {
protected:
    string basedir;
    double epsilon;
    void SetUp() override {
        basedir = "../tests/tests-generados/";
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
        if (!res) {
            cout << "autovalor equivocado [" << std::to_string(i) << "]: "
                 << solucion.first[i] << ". expected: " << expected.solucion[i] << endl;
        }
    }
    for (size_t i = 0; i < expected.n && res; ++i) {
        vector<double> vi;
        for (size_t j = 0; j < solucion.second.n(); ++j) {
            vi.emplace_back(solucion.second.at(j, i));
        }
        vector<double> tmp = mat * vi;
        res = eq(solucion.first[i] * vi, tmp, epsilon);
        if (!res) {
            cout << "autovector equivocado [" << std::to_string(i) << "]: diff";
            cout << solucion.first[i] * vi - tmp << endl;
        }
    }
    return res;
}


TEST_F(PotenciaTest, tests_diagonal) {
    for (int i = 1; i < 11; ++i) {
        string test = "diagonal_" + to_string(i);
        cout << "test " << test << ":\n";
        bool res = base_test(test + ".txt", test + ".autovalores.out");
        cout << (res ? "TRUE" : "FALSE") << endl;
        EXPECT_TRUE(res);
    }
}


TEST_F(PotenciaTest, tests_householder) {
    for (int i = 1; i < 11; ++i) {
        string test = "householder_" + to_string(i);
        cout << "test " << test << ":\n";
        bool res = base_test(test + ".txt", test + ".autovalores.out");
        cout << (res ? "TRUE" : "FALSE") << endl;
        EXPECT_TRUE(res);
    }
}


TEST_F(PotenciaTest, tests_sdp) {
    for (int i = 1; i < 11; ++i) {
        string test = "sdp_" + to_string(i);
        cout << "test " << test << ":\n";
        bool res = base_test(test + ".txt", test + ".autovalores.out");
        cout << (res ? "TRUE" : "FALSE") << endl;
        EXPECT_TRUE(res);
    }
}


TEST_F(PotenciaTest, simetrico) {
    string test = "simetrico";
    cout << "test " << test << ":\n";
    bool res = base_test(test + ".txt", test + ".autovalores.out");
    cout << (res ? "TRUE" : "FALSE") << endl;
    EXPECT_TRUE(res);
}

/*
TEST_F(PotenciaTest, karate) {
    string test = "karate";
    cout << "test " << test << ":\n";
    bool res = base_test(test + ".txt", test + ".autovalores.out");
    cout << (res ? "TRUE" : "FALSE") << endl;
    EXPECT_TRUE(res);
}*/
