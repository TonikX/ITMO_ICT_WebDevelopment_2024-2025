import {HttpException, HttpStatus, Injectable, UnauthorizedException} from '@nestjs/common';
import {JwtService} from "@nestjs/jwt";
import * as bcrypt from 'bcryptjs'
import {ArtistsService} from "../artists/artists.service";
import {Artist} from "../artists/artists.model";
import {LoginArtistDto} from "../artists/dto/login-artist.dto";
import {CreateArtistDto} from "../artists/dto/create-artist.dto";

@Injectable()
export class ArtistsAuthService {
    constructor(private artistsService: ArtistsService, private jwtService: JwtService) {}

    async login(artistDto: LoginArtistDto) {
        const artist = await this.validateArtist(artistDto)
        return this.generateToken(artist)
    }

    async registration(artistDto: CreateArtistDto) {
        const candidate = await this.artistsService.getArtistByUsername(artistDto.username);
        if (candidate) {
            throw new HttpException("Artist with this username already exists", HttpStatus.BAD_REQUEST);
        }
        const hashPassword = await bcrypt.hash(artistDto.password, 6);
        const artist = await this.artistsService.createArtist({...artistDto, password: hashPassword});
        return this.generateToken(artist)
    }

    private async generateToken(artist: Artist){
        const payload = {username: artist.username, id: artist.id};
        return {
            token: this.jwtService.sign(payload)
        }
    }

    private async validateArtist(artistDto: LoginArtistDto) {
        const artist = await this.artistsService.getArtistByUsername(artistDto.username);
        if(!artist){
            throw new HttpException("Artist not exist", HttpStatus.BAD_REQUEST);
        }
        const passwordIsEquals = await bcrypt.compare(artistDto.password, artist.password);
        if(!passwordIsEquals){
            throw new UnauthorizedException({message: "Password is incorrect"});
        }
        return artist
    }
}
