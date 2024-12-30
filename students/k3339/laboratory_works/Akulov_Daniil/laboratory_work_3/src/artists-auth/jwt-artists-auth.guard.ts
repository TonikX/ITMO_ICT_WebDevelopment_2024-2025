import {CanActivate, ExecutionContext, Injectable, UnauthorizedException} from "@nestjs/common";
import {Observable} from "rxjs";
import {JwtService} from "@nestjs/jwt";

@Injectable()
export class JwtArtistsAuthGuard implements CanActivate {
    constructor(private jwtService: JwtService) {
    }

    canActivate(context: ExecutionContext): boolean | Promise<boolean> | Observable<boolean> {
        const req = context.switchToHttp().getRequest()
        try {
            const authHeader = req.headers.authorization;
            const tokenType = authHeader.split(" ")[0];
            const token = authHeader.split(" ")[1];
            if(tokenType !== "Bearer" || !token) {
                throw new Error();
            }
            const artist = this.jwtService.verify(token);
            req.artist = artist;
            return artist;
        } catch (e){
            throw new UnauthorizedException("Unauthorized");
        }
    }
}