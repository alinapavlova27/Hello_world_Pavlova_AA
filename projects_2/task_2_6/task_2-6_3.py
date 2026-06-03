donor = input("Введите группу крови донора (I, II, III, IV): ").strip().upper()
recipient = input("Введите группу крови пациента (I, II, III, IV): ").strip().upper()
if donor == "I" or donor == recipient:
        print("Переливание возможно.")
else:
        print("Переливание невозможно.")
