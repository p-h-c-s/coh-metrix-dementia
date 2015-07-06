#!/bin/sh

KENLM_PATH=$HOME/Develop/kenlm/
CORPORA_PATH=$HOME/Develop/corpora/

cat $CORPORA_PATH/ngram_corpus_*.txt \
 | $KENLM_PATH/bin/lmplz -o 3 -S 80% -T /tmp \
 | gzip > $CORPORA_PATH/corpus_3gram.arpa.gz
