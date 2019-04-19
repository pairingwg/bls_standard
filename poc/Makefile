%.py: %.sage
	sage -preparse $<
	mv $<.py $@

all: hash_to_base.py\
	   map2curve_ft.py


test_fouquetibouchi:
	sage fouquetibouchi.sage
test_ft_bls12_381:
	sage map2curve_ft.sage
test_hash_to_base:
	sage hash_to_base.sage

test: all
	test_fouquetibouchi \
	test_ft_bls12_381 \

clean:
	rm -f *.sage.py 
