class InfoMessage():
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training():
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    CONVERT_TO_MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weigth = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # хотя, согласно задания тип тренировки должен быть записан кириллицей
        # - "тип тренировки (бег, ходьба или плавание);"
        # надо было бы прописать как self.__str__(), а не type(self).__name__
        # для этого мной были добавлены соответствующие методы в классы.

        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weigth / self.M_IN_KM
                * (self.duration * self.CONVERT_TO_MINUTES))

    def __str__(self) -> str:
        return 'бег'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    FIRST_COEF = 0.035
    SECOND_COEF = 0.029
    CONVERT_TO_MS = 0.278
    CONVERT_TO_METERS = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        speed_in_ms = self.get_mean_speed() * self.CONVERT_TO_MS
        helght_in_meters = float(self.height) / self.CONVERT_TO_METERS

        return ((self.FIRST_COEF * self.weigth
                + (speed_in_ms**2 / helght_in_meters)
                * self.SECOND_COEF * self.weigth)
                * self.duration * self.CONVERT_TO_MINUTES)

    def __str__(self) -> str:
        return 'ходьба'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    FIRST_COEF = 1.1
    SECOND_COEF = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""

        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.FIRST_COEF) * self.SECOND_COEF
                * self.weigth * self.duration)

    def __str__(self) -> str:
        return 'плавание'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    TRAINING_TYPES = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return TRAINING_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
