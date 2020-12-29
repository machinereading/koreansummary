# Korean Summary
## About
이 코드는 '사전학습 인코더 기반의 생성적 요약에서 구문과 의미 특질의 영향에 대한 연구'에서 사용된 것이고, [PreSumm](https://github.com/nlpyang/PreSumm)의 코드를 기반으로 작업한 모델입니다. 

## Prerequisite
* `python3`
* `torch 1.1.0`
* `transformers 3.4.0`
* `tqdm`

## Install
	git clone https://github.com/machinereading/koreansummary.git
	cd koreansummary   
	pip3 install -r requirements.txt

## Data Preparation For Korean
### Data
Data is came from [모두의 말뭉치](https://corpus.korean.go.kr/) and composed of list of the documents.  
Dependency and Frame semantics are parsed by [ETRI OPEN API](https://aiopen.etri.re.kr/) and [frameBERT](https://github.com/machinereading/frameBERT).   
Every documents have their id, original text, abstractive summary. 'document_id' is a id of each documents.   
'original' and 'abstractive_summary' have text, dependency, and frame parsed results for original document and human summury.   
Every dependency and frame results are in sentences. 
* sample: json_data/sample.json

#### Data Format
* document_id
* subclass
* head: news' title
* subhead: news' subtitle
* original: information of source text.
	* text: source text for a sentence
	* morp, morp_eval, WSD, word, NE, chunk, dependency, phrase_dependency, SRL, relation, SA, ZA: which are results of NLU by [ETRI OPEN API](https://aiopen.etri.re.kr/).
	* dependency
		* id: word id
		* text: word's text
		* head: head word's id
		* label
		* mod: dependents' id list
	* frame: which is results from frame semantics parsing by [frameBERT](https://github.com/machinereading/frameBERT).
		* first list means sentences words list
		* second list shows LU(Lexical Unit)
		* third list shows LU's frame 
		* fourth list shows frame arguments by BIO format
* abstractive_summary: information of abstractive summary.
* extractive_summary: information of extractive summary. 
	
#### Example
	
	[
		{
			"document_id": "sample0000000000.0",
			"subclass": "NA",
			"head": "“적자나도 주민건강 지킨다” 정선군의 도전",
			"subhead": "최승준 군수, 150병상 의료원 추진",
			"original": [
				{
					"id": 0,
					"reserve_str": "",
					"text": "“적자나도 주민건강 지킨다” 정선군의 도전",
					"morp": [...],
					"morp_eval": [...],
					"WSD": [...],
					"word": [...],
					"NE": [...],
					"chunk": [...],
					"dependency": [
						{
						"id": 0,
						"text": "“적자나도",
						"head": 2,
						"label": "NP_SBJ",
						"mod": [],
						"weight": 0.350977
						},
						...
					]
					"phrase_dependency": [...],
					"SRL": [...],
					"relation": [],
					"SA": [],
					"ZA": [],
					"frame": [
						[
							[
								"“적자나도",
								"주민건강",
								"지킨다”",
								"정선군의",
								"도전"
							],
							[
								"_",
								"_",
								"지키다.v",
								"_",
								"_"
							],
							[
								"_",
								"_",
								"Protecting",
								"_",
								"_"
							],
							[
								"O",
								"B-Asset",
								"O",
								"O",
								"O"
							]
						],
						...
					]
				}
			],
			"abstractive_summary": [...],
			"extractive_summary": [...]
		}
	]
			
### Preprocess
For data preparation, you have to make json formatted data files(korean.test.json, korean.valid.json, korean.train.json) in th same directory(JSON_PATH).  
Files have a same format of `json_data/sample.json`.  
If you want to split json files, you can split them as 'korean.test.0.json', 'korean.test.1.json', 'korean.test.2.json', ... .

	python preprocess.py -mode format_to_bert -raw_path JSON_PATH -save_path BERT_DATA_PATH  -lower -n_cpus 1 -log_file ../logs/preprocess.log
* `JSON_PATH` is the directory containing json files (`../json_data`), `BERT_DATA_PATH` is the target directory to save the generated binary files (`../bert_data`)
## Train
	python train.py -task abs -mode train -bert_data_path BERT_DATA_PATH -dec_dropout 0.2 -model_path MODEL_PATH -sep_optim true -lr_bert 0.002 -lr_dec 0.2 -save_checkpoint_steps 2000 -batch_size 140 -train_steps 50000 -report_every 50 -accum_count 10 -use_interval true -warmup_steps_bert 20000 -warmup_steps_dec 10000 -max_pos 512 -visible_gpus 1,2 -log_file ../logs/train.log -use_dep -use_frame use_bert_emb true
* If you want to use dependency or frame parsed result, add `-use_dep`, `-use_frame`.

## Evaluation
	python train.py -task abs -mode validate -test_all -batch_size 3000 -test_batch_size 500 -bert_data_path BERT_DATA_PATH -log_file ../logs/valid.log -model_path MODEL_PATH -sep_optim true -use_interval true -visible_gpus 0 -max_pos 512 -max_length 200 -alpha 0.95 -min_length 50 -result_path ../results/korean -use_dep -use_frame -use_bert_emb true
* `-mode` can be {`validate, test`}, where `validate` will inspect the model directory and evaluate the model for each newly saved checkpoint, `test` need to be used with `-test_from`, indicating the checkpoint you want to use
* `MODEL_PATH` is the directory of saved checkpoints
* use `-mode valiadte` with `-test_all`, the system will load all saved checkpoints and select the top ones to generate summaries (this will take a while)
## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://semanticweb.kaist.ac.kr/)

## Publisher
[Machine Reading Lab](http://semanticweb.kaist.ac.kr/) @ KAIST

## Contact
Kuntae Kim. `kuntaek@kaist.ac.kr`

## Acknowledgement
This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2013-0-00109, WiseKB: Big data based self-evolving knowledge base and reasoning platform)
