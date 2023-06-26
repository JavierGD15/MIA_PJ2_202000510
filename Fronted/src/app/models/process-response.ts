export class ProcessResponse<T> {
    Success: boolean = false;
    Message: string = '';
    Resource!: T;
}