#include "gtest-1.8.1/gtest.h"

#include "../src/IO.h"
#include "../src/potencia.h"


class PotenciaTest : public testing::Test {
protected:
    string basedir;
    double epsilon;
    void SetUp() override {
        basedir = "../catedra/";
        epsilon = 1e-4;
    }
};


TEST_F(PotenciaTest, test_aleatorio) {}
