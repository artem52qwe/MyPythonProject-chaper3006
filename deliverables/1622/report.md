# Память и производительность: Python и нативный модуль

Макаров Артем Александрович · 3427А

## Постановка и среда
Использована Python-программа с ctypes и собственным C-модулем: 50 вызовов выделяют по 2048 double. Флаг leak=1 намеренно пропускает free; leak=0 освобождает массив. Дополнительно исследован чистый Python-код с удержанием списков и повторным суммированием квадратов.

Valgrind не является штатным нативным инструментом Windows, а gcov работает с кодом, скомпилированным GCC, не с Python-байткодом. Поэтому из Windows подготовлены исходники, а проверка выполнена в Linux GitHub Actions. gcov ниже измеряет только собственную C-библиотеку. Установка и запуск Valgrind непосредственно в Windows не заявляются.

Воспроизводимый запуск: https://github.com/artem52qwe/MyPythonProject-chaper3006/actions/runs/40942530298

## Исходник и исправление
В режиме до исправления leak=1 динамический массив теряется после возврата. Исправленный режим leak=0 выполняет `free(values)` после вычисления результата. Возвращается значение, не указатель, поэтому освобождение безопасно. Ошибка malloc обрабатывается значением -1.0; в данном эксперименте этот путь не был вызван.

### native.c
```c
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
```

### driver.py
```python
"""Call a deliberately leaking or fixed native measurement routine."""
import ctypes
from pathlib import Path
import sys

library = ctypes.CDLL(str(Path(__file__).with_name("native.so")))
library.sample_average.argtypes = [ctypes.c_int]
library.sample_average.restype = ctypes.c_double
leak = int(sys.argv[1])
for _ in range(50):
    value = library.sample_average(leak)
assert abs(value - 24.4765625) < 0.000001, value
print("mean:", value, "native calls:", 50)
```

### native.yml
```yaml
name: Native allocation and coverage
on:
  push:
    branches: [master]
    paths: ['native/**', '.github/workflows/native.yml']
permissions:
  contents: read
jobs:
  analysis:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - run: sudo apt-get update -qq && sudo apt-get install -y valgrind
      - name: Execute before and after native calls
        working-directory: native
        run: |
          gcc -g -O0 -fPIC --coverage -shared native.c -o native.so
          valgrind --leak-check=full --show-leak-kinds=definite --log-file=before.log python3 driver.py 1
          valgrind --leak-check=full --show-leak-kinds=definite --log-file=after.log python3 driver.py 0
          gcov -b native.so-native.gcno > coverage.log
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: native-evidence
          path: |
            native/*.log
            native/*.gcov
```

## Результаты Valgrind и gcov
| Показатель | До | После |
|---|---|---|
| Definitely lost | 819200 байт, 50 блоков | 0 байт, 0 блоков |
| Вычисленный результат | 24.4765625 | 24.4765625 |
| Остаток still reachable CPython после исправления | Не критерий утечки модуля | 403083 байта, 17 блоков |
| gcov строки C | Оба режима вызваны общим прогоном | 100% из 10 |
| Ветви выполнены / taken at least once | Совместное покрытие | 100% / 83.33% из 6 |

Последний показатель означает, что один исход ветвления, отказ malloc, не пройден. Покрытие не доказывает правильность, а gcov не измеряет скорость. still reachable отличается от definitely lost; память интерпретатора не объявляется устранённой утечкой собственной библиотеки.

## Дополнительная оптимизация Python
До: для каждого прохода хранится новый список и повторяется сумма квадратов. После: используется целочисленная формула суммы квадратов, массивы не создаются. Контракт — неотрицательные целые rounds и size, как в стенде. Python before освобождает списки после возврата: это избыточное удержание памяти во время работы, а не потерянный native-указатель.

| Измерение: 80 × 3000, пять повторений | До | После |
|---|---|---|
| Медиана секунд с tracemalloc | 0.203744 | 0.000003 |
| Максимальный пик байт tracemalloc | 8947804 | 96 |
| Результат | 719640040000 | 719640040000 |

Равенство проверено также для размеров 0, 1, 2, 19 и 3000. Замеры относятся к локальному процессу с включённым tracemalloc; это не универсальная оценка производительности. Устранены повторные вычисления и линейное удержание списков.

### benchmark.py
```python
"""Compare retained lists with a closed-form sum; no external services."""
import json
import statistics
import time
import tracemalloc


def before(rounds=80, size=3000):
    retained = []
    total = 0
    for _ in range(rounds):
        values = list(range(size))
        retained.append(values)
        total += sum(value * value for value in values)
    return total


def after(rounds=80, size=3000):
    return rounds * (size - 1) * size * (2 * size - 1) // 6


def measure(function):
    times = []
    peak = 0
    for _ in range(5):
        tracemalloc.start()
        start = time.perf_counter()
        result = function()
        times.append(time.perf_counter() - start)
        peak = max(peak, tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return {"result": result, "median_seconds": statistics.median(times),
            "peak_bytes": peak}


if __name__ == "__main__":
    for n in (0, 1, 2, 19, 3000):
        assert before(3, n) == after(3, n)
    results = {"before": measure(before), "after": measure(after)}
    assert results["before"]["result"] == results["after"]["result"]
    print(json.dumps(results, indent=2))
```

### before.log
```text
==2538== Memcheck, a memory error detector
==2538== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==2538== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==2538== Command: python3 driver.py 1
==2538== Parent PID: 2532
==2538== 
==2538== 
==2538== HEAP SUMMARY:
==2538==     in use at exit: 1,222,283 bytes in 67 blocks
==2538==   total heap usage: 4,061 allocs, 3,994 frees, 10,959,961 bytes allocated
==2538== 
==2538== 16,384 bytes in 1 blocks are definitely lost in loss record 11 of 14
==2538==    at 0x484A888: malloc (vg_replace_malloc.c:447)
==2538==    by 0x5A394B3: sample_average (native.c:6)
==2538==    by 0x5A4A055: ??? (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A45D12: ??? (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A488ED: ffi_call (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A248BA: ??? (in /usr/lib/python3.14/lib-dynload/_ctypes.cpython-314-x86_64-linux-gnu.so)
==2538==    by 0x5A25314: ??? (in /usr/lib/python3.14/lib-dynload/_ctypes.cpython-314-x86_64-linux-gnu.so)
==2538==    by 0x53035B: _PyObject_MakeTpCall (in /usr/bin/python3.14)
==2538==    by 0x551897: _PyEval_EvalFrameDefault (in /usr/bin/python3.14)
==2538==    by 0x548BC5: PyEval_EvalCode (in /usr/bin/python3.14)
==2538==    by 0x6C9730: ??? (in /usr/bin/python3.14)
==2538==    by 0x6C62D0: ??? (in /usr/bin/python3.14)
==2538== 
==2538== 802,816 bytes in 49 blocks are definitely lost in loss record 14 of 14
==2538==    at 0x484A888: malloc (vg_replace_malloc.c:447)
==2538==    by 0x5A394B3: sample_average (native.c:6)
==2538==    by 0x5A4A055: ??? (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A45D12: ??? (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A488ED: ffi_call (in /usr/lib/x86_64-linux-gnu/libffi.so.8.2.0)
==2538==    by 0x5A248BA: ??? (in /usr/lib/python3.14/lib-dynload/_ctypes.cpython-314-x86_64-linux-gnu.so)
==2538==    by 0x5A25314: ??? (in /usr/lib/python3.14/lib-dynload/_ctypes.cpython-314-x86_64-linux-gnu.so)
==2538==    by 0x53035B: _PyObject_MakeTpCall (in /usr/bin/python3.14)
==2538==    by 0x54E854: _PyEval_EvalFrameDefault (in /usr/bin/python3.14)
==2538==    by 0x548BC5: PyEval_EvalCode (in /usr/bin/python3.14)
==2538==    by 0x6C9730: ??? (in /usr/bin/python3.14)
==2538==    by 0x6C62D0: ??? (in /usr/bin/python3.14)
==2538== 
==2538== LEAK SUMMARY:
==2538==    definitely lost: 819,200 bytes in 50 blocks
==2538==    indirectly lost: 0 bytes in 0 blocks
==2538==      possibly lost: 0 bytes in 0 blocks
==2538==    still reachable: 403,083 bytes in 17 blocks
==2538==         suppressed: 0 bytes in 0 blocks
==2538== Reachable blocks (those to which a pointer was found) are not shown.
==2538== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==2538== 
==2538== For lists of detected and suppressed errors, rerun with: -s
==2538== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```

### after.log
```text
==2539== Memcheck, a memory error detector
==2539== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==2539== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==2539== Command: python3 driver.py 0
==2539== Parent PID: 2532
==2539== 
==2539== 
==2539== HEAP SUMMARY:
==2539==     in use at exit: 403,083 bytes in 17 blocks
==2539==   total heap usage: 4,061 allocs, 4,044 frees, 10,959,961 bytes allocated
==2539== 
==2539== LEAK SUMMARY:
==2539==    definitely lost: 0 bytes in 0 blocks
==2539==    indirectly lost: 0 bytes in 0 blocks
==2539==      possibly lost: 0 bytes in 0 blocks
==2539==    still reachable: 403,083 bytes in 17 blocks
==2539==         suppressed: 0 bytes in 0 blocks
==2539== Reachable blocks (those to which a pointer was found) are not shown.
==2539== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==2539== 
==2539== For lists of detected and suppressed errors, rerun with: -s
==2539== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

### coverage.log
```text
File 'native.c'
Lines executed:100.00% of 10
Branches executed:100.00% of 6
Taken at least once:83.33% of 6
No calls
Creating 'native.c.gcov'

Lines executed:100.00% of 10
```

### native.c.gcov
```text
-:    0:Source:native.c
        -:    0:Graph:native.so-native.gcno
        -:    0:Data:native.so-native.gcda
        -:    0:Runs:2
        -:    1:#include <stdlib.h>
        -:    2:#include <stddef.h>
        -:    3:
        -:    4:/* leak=1 intentionally loses a native allocation for the before experiment. */
function sample_average called 100 returned 100% blocks executed 89%
      100:    5:double sample_average(int leak) {
      100:    6:    double *values = malloc(2048 * sizeof(double));
     100*:    7:    if (values == NULL) return -1.0;
branch  0 taken 0% (fallthrough)
branch  1 taken 100%
      100:    8:    double sum = 0.0;
   204900:    9:    for (size_t i = 0; i < 2048; ++i) {
branch  0 taken 100%
branch  1 taken 1% (fallthrough)
   204800:   10:        values[i] = (double)(i % 50);
   204800:   11:        sum += values[i];
        -:   12:    }
      100:   13:    double result = sum / 2048.0;
      100:   14:    if (!leak) free(values);
branch  0 taken 50% (fallthrough)
branch  1 taken 50%
      100:   15:    return result;
        -:   16:}
```

## Источники
- Платформы Valgrind: https://valgrind.org/info/platforms.html
- GCC gcov: https://gcc.gnu.org/onlinedocs/gcc/Gcov.html
- tracemalloc: https://docs.python.org/3/library/tracemalloc.html
