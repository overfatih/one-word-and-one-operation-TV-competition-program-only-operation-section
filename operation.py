import random
from itertools import combinations

# Rastgele sayıları üretme fonksiyonu
def generate_random_numbers():
    single_digits = random.choices(range(1, 10), k=5)  # 1-9 arasından 5 sayı
    double_digit = random.randint(1, 9) * 10  # 10 ve 10'un katlarından iki basamaklı bir sayı
    return single_digits + [double_digit]  # Liste olarak döndür

# Rastgele 3 basamaklı hedef sayı üretme
def generate_target():
    return random.randint(100, 999)

# Dört işlem fonksiyonu
def apply_operations(a, b):
    results = []
    results.append((' + ', a + b))  # Toplama
    results.append((' - ', a - b))  # Çıkarma
    results.append((' - ', b - a))  # Çıkarma (tersi)
    results.append((' * ', a * b))  # Çarpma
    if b != 0 and a % b == 0:
        results.append((' / ', a // b))  # Bölme (tam bölünüyorsa)
    if a != 0 and b % a == 0:
        results.append((' / ', b // a))  # Bölme (tam bölünüyorsa)
    return results

# Backtracking ile hedefi bulma
def find_target(numbers, target, used_numbers=set(), steps=[], closest_result=None, closest_steps=None):
    if target in numbers:
        print(f"✅ Tam sonuç: {target} elde edilebiliyor!")
        for step in steps:
            print(f"🔹 {step[0]} {step[1]} {step[2]} = {step[3]}")
        return True, closest_result, closest_steps

    for a, b in combinations(numbers, 2):  # İkili sayıları seç
        new_numbers = numbers.copy()
        new_numbers.remove(a)
        new_numbers.remove(b)
        for op, result in apply_operations(a, b):  # Dört işlem uygula
            if result not in used_numbers:
                used_numbers.add(result)
                new_numbers.append(result)  # Yeni sonucu ekleyerek ilerle
                steps.append((a, op, b, result))  # Adım ekle
                if result == target:  # Hedefe tam ulaşınca erken çık
                    print(f"✅ Tam sonuç: {target} elde edilebiliyor!")
                    for step in steps:
                        print(f"🔹 {step[0]} {step[1]} {step[2]} = {step[3]}")
                    return True, closest_result, closest_steps
                # En yakın sonuç hesaplaması
                if closest_result is None or abs(target - result) < abs(target - closest_result):
                    closest_result = result
                    closest_steps = steps.copy()
                # Rekürsif olarak devam et
                found, closest_result, closest_steps = find_target(new_numbers, target, used_numbers, steps, closest_result, closest_steps)
                if found:
                    return found, closest_result, closest_steps
                steps.pop()  # Sonucu geri al
                new_numbers.remove(result)  # Geri al
                used_numbers.remove(result)
    return False, closest_result, closest_steps

# Rastgele veri üret
numbers = generate_random_numbers()
target = generate_target()

print(f"🎲 Rastgele Sayılar: {sorted(numbers)}")
print(f"🎯 Hedef Sayı: {target}")

# Çalıştır
found, closest_result, closest_steps = find_target(numbers, target)

# Hedef bulunamadıysa en yakın sonucu yazdır
if not found:
    if closest_result is not None:
        print(f"⚠️ {abs(closest_result-target)} yaklaşık. En yakın sonuç: {closest_result}")
        if abs(closest_result-target) < 9:
            for step in closest_steps:
                print(f"🔹 {step[0]} {step[1]} {step[2]} = {step[3]}")
        else:
            print(" ❌ İşlem sonucu en fazla (+/-)9 fark olabilir. Kaybettin...")
    else:
        print(f"❌ Hedefe ulaşılamadı! Daha iyi bir sonuç bulunamadı.")
