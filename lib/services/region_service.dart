import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/tag.dart';

class RegionService {
  static List<RegionTag>? _cachedRegions;

  static Future<List<RegionTag>> loadRegionTags() async {
    if (_cachedRegions != null) {
      return _cachedRegions!;
    }

    try {
      // JSON 파일 로드
      final String jsonString = await rootBundle.loadString('assets/regions.json');
      final List<dynamic> jsonData = json.decode(jsonString);
      
      // JSON 데이터를 RegionTag 객체로 변환
      final List<RegionTag> regionTags = jsonData.map((json) {
        return RegionTag(
          name: json['name'] as String,
          level: json['level'] as int,
          parentRegion: json['parentRegion'] as String?,
          code: json['code'] as String?,
        );
      }).toList();

      _cachedRegions = regionTags;
      return regionTags;
    } catch (e) {
      print('지역 데이터 로드 중 오류 발생: $e');
      rethrow;
    }
  }

  static List<RegionTag> getRegionsByLevel(List<RegionTag> regions, int level) {
    return regions.where((region) => region.level == level).toList();
  }

  static List<RegionTag> getChildRegions(List<RegionTag> regions, String parentName) {
    return regions.where((region) => region.parentRegion == parentName).toList();
  }

  static List<RegionTag> getParentRegions(List<RegionTag> regions) {
    return regions.where((region) => region.level == 1).toList();
  }

  static List<RegionTag> getMiddleRegions(List<RegionTag> regions) {
    return regions.where((region) => region.level == 2).toList();
  }

  static List<RegionTag> getBottomRegions(List<RegionTag> regions) {
    return regions.where((region) => region.level == 3).toList();
  }
} 