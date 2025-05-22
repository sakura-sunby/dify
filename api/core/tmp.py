# indexing_runner.py

import json

...

def indexing_estimate(
    self,
    tenant_id: str,
    extract_settings: list[ExtractSetting],
    tmp_processing_rule: dict,
    doc_form: Optional[str] = None,
    doc_language: str = "English",
    dataset_id: Optional[str] = None,
    indexing_technique: str = "economy",
    split_strategy: Optional[str] = None,
) -> IndexingEstimate:
    ...

    external_strategy_url = None
    if split_strategy:
        try:
            strategy_dict = json.loads(split_strategy)
            if strategy_dict.get("type") == "external":
                external_strategy_url = strategy_dict.get("external_strategy_url")
        except Exception as e:
            logging.warning(f"Failed to parse split_strategy: {str(e)}")

    # 创建 index_processor
    index_type = doc_form
    index_processor_config = {}
    if external_strategy_url:
        index_processor_config["server_address"] = external_strategy_url

    index_processor = IndexProcessorFactory(index_type, config_options=index_processor_config).init_index_processor()

    for extract_setting in extract_settings:
        # extract
        processing_rule = DatasetProcessRule(
            mode=tmp_processing_rule["mode"], rules=json.dumps(tmp_processing_rule["rules"])
        )

        # 👇 将 external_strategy_url 传入 extract 方法
        text_docs = index_processor.extract(
            extract_setting,
            process_rule_mode=tmp_processing_rule["mode"],
            external_strategy_url=external_strategy_url
        )
        ...
