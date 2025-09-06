from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from models.models import User, Title, DubberTitle, Report, ForceMajeure


class DubberService:
    """Сервис для работы с функционалом даббера"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_titles(self, user_id: int) -> List[Title]:
        """
        Получить все тайтлы, назначенные пользователю
        Args:
            user_id: ID пользователя
        Returns:
            List[Title]: Список тайтлов пользователя
        """
        return self.db.query(Title).join(DubberTitle).filter(
            DubberTitle.dubber_id == user_id
        ).all()

    def get_title_by_id(self, title_id: int) -> Optional[Title]:
        """
        Получить тайтл по ID
        Args:
            title_id: ID тайтла
        Returns:
            Optional[Title]: Объект тайтла или None
        """
        return self.db.query(Title).filter(Title.id == title_id).first()

    def create_report(self, user_id: int, title_id: int, episode: int,
                      status: str, comment: Optional[str] = None) -> Report:
        """
        Создать отчет о сдаче серии
        Args:
            user_id: ID даббера
            title_id: ID тайтла
            episode: Номер серии
            status: Статус сдачи ('submitted' или 'delayed')
            comment: Комментарий при задержке
        Returns:
            Report: Созданный отчет
        """
        # Получаем тайтл для расчета дедлайна
        title = self.get_title_by_id(title_id)

        # Расчет дедлайна (2 дня с момента выхода серии)
        # В реальной системе здесь должна быть логика определения времени выхода серии
        deadline = datetime.now() + timedelta(days=2)

        report = Report(
            dubber_id=user_id,
            title_id=title_id,
            episode=episode,
            status=status,
            comment=comment,
            submitted_at=datetime.now() if status == 'submitted' else None,
            deadline=deadline
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_user_debts(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Получить список долгов пользователя
        Args:
            user_id: ID пользователя
        Returns:
            List[Dict]: Список словарей с информацией о долгах
        """
        titles = self.get_user_titles(user_id)
        debts = []

        for title in titles:
            if title.current_episode == 0:
                continue  # Пропускаем тайтлы без текущей серии

            # Ищем отчет для текущей серии
            report = self.db.query(Report).filter(
                and_(
                    Report.dubber_id == user_id,
                    Report.title_id == title.id,
                    Report.episode == title.current_episode
                )
            ).first()

            status = "submitted" if report and report.status == 'submitted' else "not_submitted"
            is_delayed = True if report and report.status == 'delayed' else False

            debts.append({
                'title_id': title.id,
                'title_name': title.name,
                'episode': title.current_episode,
                'status': status,
                'is_delayed': is_delayed,
                'submitted_at': report.submitted_at if report else None,
                'comment': report.comment if report else None
            })

        return debts

    def create_force_majeure(self, user_id: int, message: str) -> ForceMajeure:
        """
        Создать запись о форс-мажоре
        Args:
            user_id: ID пользователя
            message: Сообщение о форс-мажоре
        Returns:
            ForceMajeure: Созданная запись
        """
        force_majeure = ForceMajeure(
            user_id=user_id,
            message=message
        )

        self.db.add(force_majeure)
        self.db.commit()
        self.db.refresh(force_majeure)
        return force_majeure

    def update_user_role(self, user_id: int, new_role: str) -> Optional[User]:
        """
        Обновить роль пользователя
        Args:
            user_id: ID пользователя
            new_role: Новая роль ('dubber', 'timer', 'admin')
        Returns:
            Optional[User]: Обновленный пользователь или None
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.role = new_role
            self.db.commit()
            self.db.refresh(user)
        return user

    def get_episode_report(self, user_id: int, title_id: int, episode: int) -> Optional[Report]:
        """
        Получить отчет по конкретной серии
        Args:
            user_id: ID даббера
            title_id: ID тайтла
            episode: Номер серии
        Returns:
            Optional[Report]: Найденный отчет или None
        """
        return self.db.query(Report).filter(
            and_(
                Report.dubber_id == user_id,
                Report.title_id == title_id,
                Report.episode == episode
            )
        ).first()

    def has_title_access(self, user_id: int, title_id: int) -> bool:
        """
        Проверить, есть ли у пользователя доступ к тайтлу
        Args:
            user_id: ID пользователя
            title_id: ID тайтла
        Returns:
            bool: True если есть доступ, False если нет
        """
        return self.db.query(DubberTitle).filter(
            and_(
                DubberTitle.dubber_id == user_id,
                DubberTitle.title_id == title_id
            )
        ).first() is not None