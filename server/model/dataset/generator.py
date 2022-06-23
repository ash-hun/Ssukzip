import requests
from bs4 import BeautifulSoup
import time
import csv

need_reviews_cnt = 10380
reviews = []
review_data=[]
url = 'https://movie.naver.com/movie/point/af/list.naver?&page='

def generating():
    for page in range(1,1000):
        html = requests.get(url+str(page))
        soup = BeautifulSoup(html.content,'html.parser')
        reviews = soup.find_all("td",{"class":"title"})
        
        for review in reviews:
            sentence = review.find("a",{"class":"report"}).get("onclick").split("', '")[2]
            if sentence != "":
                movie = review.find("a",{"class":"movie color_b"}).get_text()
                score = review.find("em").get_text()
                review_data.append([movie,sentence,int(score)])
                need_reviews_cnt-= 1
        if need_reviews_cnt < 0:                                         
            break
        time.sleep(0.5)

    columns_name = ["movie","sentence","score"]
    with open ( "./sample.csv", "w", newline ="", encoding = 'utf-8-sig' ) as f:
        write = csv.writer(f)
        write.writerow(columns_name)
        write.writerows(review_data)

class RawMovieReview:
    def __init__(self, file_name:str="sample.csv"):
        self.file_name = file_name

    def Indexing(self, N):
        f = open(self.file_name, "r", encoding="utf8")
        dataset = csv.reader(f)
        cnt = 0
        next(dataset)
        for item in dataset:
            if cnt == N-1:
                res = tuple(item)
                f.close()
                return res
            else:
                cnt += 1
    
    def Length(self):
        f = open(self.file_name, "r", encoding="utf8")
        dataset = csv.reader(f)
        length = 0
        for _ in dataset:
            length += 1
        return length-1

class MovieReview(RawMovieReview):
    def __init__(self, score_threadhold:int):
        self.score_threadhold = score_threadhold
    
    def Indexing(self, N):
        f = open("./sample.csv", "r", encoding="utf8")
        reader = csv.reader(f)
        cnt = 0
        next(reader)
        for item in reader:
            if cnt == N-1:
                if int(item[2])>self.score_threadhold:
                    res = tuple([item[1].strip(), True])
                else:
                    res = tuple([item[1].strip(), False])
                f.close()
                return res
            else:
                cnt += 1

#======================================================================================================================

def generating_data():
    samples = []
    page_id = 1

    while len(samples) < 1000:
        url = f'https://movie.naver.com/movie/point/af/list.naver?&page={page_id}'
        res = requests.get(url)
        soup = BeautifulSoup(
            res.text,
            'html.parser'
        )
        
        for td in soup.find_all('td', attrs={"class": "title"}):
            samples.append((td.a.string, td.br.next_element.rstrip(), int(td.div.em.string)))
        time.sleep(.5)
        page_id +=  1

    with open('samples.csv', 'w') as fd:
        writer = csv.writer(fd)
        writer.writerow(['movie', 'sentence', 'score'])
        writer.writerows(samples) 

class OriginDataForm:
    def __init__(self, file_name: str="sample.csv"):
        with open(file_name, 'r') as fd:
            fd.readline()
            reader = csv.reader(fd)
            self._samples = [
                (movie, sentence, int(score))
                for movie, sentence, score
                in reader
            ]

    def __len__(self):
        return len(self._samples)
    
    def __getitem__(self, index):
        return self._samples[index]

class setData(OriginDataForm):
    def __init__(self, score_threadhold: int, file_name: str="samples.csv"):
        super().__init__(file_name)
        self._score_threadhold = score_threadhold

    def __getitem__(self, index):
        _, sentence, score = super().__getitem__(index)
        return sentence, score >= self._score_threadhold


if __name__=="__main__":
    myRaw = RawMovieReview("sample.csv")
    print(f"myRaw.Indexing(3) : {myRaw.Indexing(3)}")
    print(f"myRaw.Length() : {myRaw.Length()}")
    myMovie = MovieReview(5)
    print(f"myMovie.Indexing(3) : {myMovie.Indexing(3)}")
    print("="*100)
    raw_dataset = OriginDataForm()
    raw_dataset = setData(7)
