from concurrent import futures
import random
import grpc

from recommendations_pb2 import BookCategory, BookRecommendation, RecommendationResponse
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
        BookRecommendation(id=4, title="Автостопом по галактике"),
        BookRecommendation(id=5, title="Игра Эндера"),
        BookRecommendation(id=6, title="Тайна Сомбреро"),
        BookRecommendation(id=7, title="Десять негритят"),
        BookRecommendation(id=8, title="Знак четырех"),
        BookRecommendation(id=9, title="Седьмая печать"),
        BookRecommendation(id=10, title="Преступление и наказание"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=11, title="Дюна"),
        BookRecommendation(id=12, title="Гиперион"),
        BookRecommendation(id=13, title="Основание"),
        BookRecommendation(id=14, title="Война миров"),
        BookRecommendation(id=15, title="Автостопом по галактике"),
        BookRecommendation(id=16, title="Игра Эндера"),
        BookRecommendation(id=17, title="Ночной дозор"),
        BookRecommendation(id=18, title="Солярис"),
        BookRecommendation(id=19, title="1984"),
        BookRecommendation(id=20, title="Марсианин"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
        BookRecommendation(id=23, title="Человек в поисках смысла"),
        BookRecommendation(id=24, title="Думай и богатей"),
        BookRecommendation(id=25, title="Метод Помодоро"),
        BookRecommendation(id=26, title="Код да Винчи"),
        BookRecommendation(id=27, title="Путь к свободе"),
        BookRecommendation(id=28, title="Богатый папа, бедный папа"),
        BookRecommendation(id=29, title="Мастер и Маргарита"),
        BookRecommendation(id=30, title="Алхимик"),
    ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)
        return RecommendationResponse(recommendations=books_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()