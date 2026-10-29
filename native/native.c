#include <stdlib.h>
#include <stddef.h>

/* leak=1 intentionally loses a native allocation for the before experiment. */
double sample_average(int leak) {
    double *values = malloc(2048 * sizeof(double));
    if (values == NULL) return -1.0;
    double sum = 0.0;
    for (size_t i = 0; i < 2048; ++i) {
        values[i] = (double)(i % 50);
        sum += values[i];
    }
    double result = sum / 2048.0;
    if (!leak) free(values);
    return result;
}
