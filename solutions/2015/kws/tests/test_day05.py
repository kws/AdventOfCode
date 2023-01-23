from aoc_2015_kws.day_05 import *


def test_has_three_vowels():
    assert has_three_vowels("aei")
    assert has_three_vowels("xazegov")
    assert has_three_vowels("aeiouaeiouaeiou")
    assert not has_three_vowels("dvszwmarrgswjxmb")


def test_has_repeating_letter():
    assert has_repeating_letter("xx")
    assert has_repeating_letter("abcdde")
    assert has_repeating_letter("aabbccdd")
    assert not has_repeating_letter("jchzalrnumimnmhp")
    assert not has_repeating_letter("haegwjzuvuy")


def test_has_naughty_string():
    assert has_naughty_string("haegwjzuvuyypxyu")
    assert not has_naughty_string("ugknbfddgicrmopn")


def test_is_nice():
    assert nice_or_naughty("ugknbfddgicrmopn") is Child.NICE
    assert nice_or_naughty("aaa") is Child.NICE
    assert nice_or_naughty("jchzalrnumimnmhp") is Child.NAUGHTY
    assert nice_or_naughty("haegwjzuvuyypxyu") is Child.NAUGHTY
    assert nice_or_naughty("dvszwmarrgswjxmb") is Child.NAUGHTY


def test_has_repeating_pair():
    assert has_repeating_pair("xyxy")
    assert has_repeating_pair("aabcdefgaa")
    assert not has_repeating_pair("aaa")


def test_repeating_letter_with_gap():
    assert has_repeating_letter_with_gap("xyx")
    assert has_repeating_letter_with_gap("abcdefeghi")
    assert has_repeating_letter_with_gap("aaa")


def test_is_nice2():
    assert nice_or_naughty2("qjhvhtzxzqqjkmpb") is Child.NICE
    assert nice_or_naughty2("xxyxx") is Child.NICE
    assert nice_or_naughty2("uurcxstgmygtbstg") is Child.NAUGHTY
    assert nice_or_naughty2("ieodomkazucvgmuy") is Child.NAUGHTY
