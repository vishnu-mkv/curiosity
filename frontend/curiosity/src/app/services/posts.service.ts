import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {apiURL} from "../../environments/environment";
import {Observable} from "rxjs";
import {post} from "../interfaces";
import {AuthService} from "./auth.service";


interface postSubmit {
    status: string,
    message?: string
}


interface postDelete {
    delete: boolean,
    message: string,
    slug: string
}

@Injectable({
    providedIn: 'root'
})
export class PostsService {

    constructor(private http: HttpClient, private auth: AuthService) {
    }

    getWriterPosts(): Observable<any> {
        return this.http.get<post[]>(apiURL + 'api/users/posts');
    }

    unSubmit(slug: string) {
        return this.http.delete<postSubmit>(apiURL + `posts/${slug}/submit/`);
    }

    submitPost(slug: string) {
        return this.http.post<postSubmit>(apiURL + `posts/${slug}/submit/`, {'submit': true});
    }

    deletePost(slug: string) {
        return this.http.delete<postDelete>(apiURL + `posts/${slug}/`);
    }
}
