twitter_results:
	for i in `seq 0 9`; do make models/twitter.$$i.model; done
	for i in `seq 0 9`; do make models/twitter.$$i.params; done
	for i in `seq 0 9`; do make models/twitter.$$i.ustr; done
	for i in `seq 0 9`; do make results/twitter.$$i.test.pred; done
	for i in `seq 0 9`; do make results/twitter.$$i.test.no_dict; done
	for i in `seq 0 9`; do make results/twitter.$$i.test.dict; done
	for i in `seq 0 9`; do make results/twitter.$$i.test.no_dict.eval; done
	for i in `seq 0 9`; do make results/twitter.$$i.test.dict.eval; done
	make results/twitter.no_dict.cival
	make results/twitter.dict.cival

klk_results:
	for i in `seq 0 9`; do make models/klk.$$i.model; done
	for i in `seq 0 9`; do make models/klk.$$i.params; done
	for i in `seq 0 9`; do make models/klk.$$i.ustr; done
	for i in `seq 0 9`; do make results/klk.$$i.test.pred; done
	for i in `seq 0 9`; do make results/klk.$$i.test.no_dict; done
	for i in `seq 0 9`; do make results/klk.$$i.test.dict; done
	for i in `seq 0 9`; do make results/klk.$$i.test.no_dict.eval; done
	for i in `seq 0 9`; do make results/klk.$$i.test.dict.eval; done
	make results/klk.no_dict.cival
	make results/klk.dict.cival

models/%.lc:data/%.train
	cat $^ | ./bin/make_label_dict.py $@

%.feats:%
	cat $^ | ./bin/extract_features.py > $@

data/%.train+dev.feats: data/%.train.feats data/%.dev.feats
	cat $^ > $@

models/%.model:data/%.config data/%.train+dev.feats data/%.dev.feats
	finnpos-train $^ $@

%.params:%.model
	finnpos-print-params $^ | ./bin/rm_config_info.py > $@

%.ustr:%.params
	cat $^ | ./bin/compile_fst_model.py $*

%.in:%
	cat $^ | cut -f1 | ./bin/pre_test_data.sh > $@

results/%.test.pred:models/%.ustr models/%.lc data/%.test.in
	cat data/$*.test.in | ./bin/predict.py models/$* 80 > $@

%.no_dict:%.pred
	cat $^ | ./bin/select_first.py > $@

results/twitter.%.test.dict:results/twitter.%.test.pred models/twitter.ol
	cat $< | ./bin/select_first_in_dict.py models/twitter.ol 80 > $@

results/klk.%.test.dict:results/klk.%.test.pred models/klk.ol
	cat $< | ./bin/select_first_in_dict.py models/klk.ol 5 > $@

%.test.gold:%.test
	cat $^ | tr -d ' ' | tr '\t' ' ' > $@

results/%.test.no_dict.eval:results/%.test.no_dict data/%.test.gold
	./bin/eval_cr.py $^ > $@

results/%.test.dict.eval:results/%.test.dict data/%.test.gold
	./bin/eval_cr.py $^ > $@

results/klk.%.cival:results/klk.0.test.%.eval
	cat results/klk.*.test.$*.eval | grep "Correction Rate" | sed 's/.*: //' | ./bin/compute_cival.py > $@

results/twitter.%.cival:results/twitter.0.test.%.eval
	cat results/twitter.*.test.$*.eval | grep "Correction Rate" | sed 's/.*: //' | ./bin/compute_cival.py > $@