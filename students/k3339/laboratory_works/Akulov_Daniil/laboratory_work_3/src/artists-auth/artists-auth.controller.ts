import {Body, Controller, Post} from '@nestjs/common';
import {ArtistsAuthService} from "./artists-auth.service";
import {LoginArtistDto} from "../artists/dto/login-artist.dto";
import {CreateArtistDto} from "../artists/dto/create-artist.dto";
import {ApiOperation, ApiResponse} from "@nestjs/swagger";

@Controller('artists-auth')
export class ArtistsAuthController {
    constructor(private readonly artistsAuthService: ArtistsAuthService) {}

    @ApiOperation({summary: 'Login as artist'})
    @ApiResponse({status: 200, type: String})
    @Post('/login')
    login(@Body() artistDto: LoginArtistDto) {
        return this.artistsAuthService.login(artistDto)
    }

    @ApiOperation({summary: 'Registration new artist'})
    @ApiResponse({status: 200, type: String})
    @Post('/registration')
    registration(@Body() artistDto: CreateArtistDto) {
        return this.artistsAuthService.registration(artistDto)
    }
}
