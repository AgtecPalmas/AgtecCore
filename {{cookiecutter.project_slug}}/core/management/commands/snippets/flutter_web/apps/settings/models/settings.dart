class SettingsModels {
  String? id;
  String? name;
  String? value;
  String? type;
  String? description;
  bool? isActive;

  SettingsModels({
    this.id,
    this.name,
    this.value,
    this.type,
    this.description,
    this.isActive,
  });

  factory SettingsModels.fromJson(Map<String, dynamic> data) {
    return SettingsModels(
      id: data.containsKey('id') ? data['id'] : '',
      name: data.containsKey('name') ? data['name'] : '',
      value: data.containsKey('value') ? data['value'] : '',
      type: data.containsKey('type') ? data['type'] : '',
      description: data.containsKey('description') ? data['description'] : '',
      isActive: data.containsKey('is_active') ? data['is_active'] : false,
    );
  }

  Map<String, dynamic> toMap() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id'] = id;
    data['name'] = name;
    data['value'] = value;
    data['type'] = type;
    data['description'] = description;
    data['is_active'] = isActive;
    return data;
  }

  /// Método para implementar o CopyWith
  /// 
  /// 
  SettingsModels copyWith({
    String? id,
    String? name,
    String? value,
    String? type,
    String? description,
    bool? isActive,
  }) {
    return SettingsModels(
      id: id ?? this.id,
      name: name ?? this.name,
      value: value ?? this.value,
      type: type ?? this.type,
      description: description ?? this.description,
      isActive: isActive ?? this.isActive,
    );
  }
}
